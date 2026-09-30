"""Uploaded images: a replaced image needs approval again, and uploads have a size limit."""

import io
import os
import shutil
import tempfile

from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from PIL import Image

from characters.forms.core.limited_edit import LimitedHumanEditForm
from characters.models.core.human import Human
from characters.models.mage.mage import Mage
from characters.services.mage_xp import spend_mage_xp
from core.constants import ImageStatus
from core.validators import validate_image_upload_size


def png_upload(name="portrait.png", side=2):
    buffer = io.BytesIO()
    Image.frombytes("RGB", (side, side), os.urandom(side * side * 3)).save(buffer, format="PNG")
    return SimpleUploadedFile(name, buffer.getvalue(), content_type="image/png")


class MediaRootMixin:
    def setUp(self):
        super().setUp()
        media_root = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, media_root, ignore_errors=True)
        settings_override = override_settings(MEDIA_ROOT=media_root)
        settings_override.enable()
        self.addCleanup(settings_override.disable)


class ReplacedImageStatusTests(MediaRootMixin, TestCase):
    def setUp(self):
        super().setUp()
        human = Human.objects.create(name="Portrait", image=png_upload())
        Human.objects.filter(pk=human.pk).update(image_status=ImageStatus.APPROVED)
        self.human = Human.objects.get(pk=human.pk)

    def test_replacing_the_image_resets_an_approved_status(self):
        self.human.image = png_upload("new.png")
        self.human.save()
        self.human.refresh_from_db()
        self.assertEqual(self.human.image_status, ImageStatus.SUBMITTED)

    def test_other_saves_keep_the_approval(self):
        self.human.name = "Renamed"
        self.human.save()
        self.human.refresh_from_db()
        self.assertEqual(self.human.image_status, ImageStatus.APPROVED)

    def test_an_explicit_status_in_the_same_save_is_kept(self):
        self.human.image = png_upload("new.png")
        self.human.image_status = ImageStatus.UNAPPROVED
        self.human.save()
        self.human.refresh_from_db()
        self.assertEqual(self.human.image_status, ImageStatus.UNAPPROVED)

    def test_approving_after_a_replacement_sticks(self):
        self.human.image = png_upload("new.png")
        self.human.save()
        self.human.image_status = ImageStatus.APPROVED
        self.human.save()
        self.human.refresh_from_db()
        self.assertEqual(self.human.image_status, ImageStatus.APPROVED)

    def test_owner_upload_through_the_limited_form_needs_approval_again(self):
        form = LimitedHumanEditForm(
            data={"name": "Portrait", "concept": "", "notes": "", "description": ""},
            files={"image": png_upload("owner.png")},
            instance=self.human,
        )
        self.assertTrue(form.is_valid(), form.errors)
        form.save()
        self.human.refresh_from_db()
        self.assertEqual(self.human.image_status, ImageStatus.SUBMITTED)

    def test_mage_sheet_image_upload_needs_approval_again(self):
        mage = Mage.objects.create(name="Sheet mage", image=png_upload())
        Mage.objects.filter(pk=mage.pk).update(image_status=ImageStatus.APPROVED)
        mage = Mage.objects.get(pk=mage.pk)
        spend_mage_xp(mage, {"category": "Image", "image_field": png_upload("sheet.png")})
        mage.refresh_from_db()
        self.assertEqual(mage.image_status, ImageStatus.SUBMITTED)


@override_settings(MAX_IMAGE_UPLOAD_SIZE=1024)
class ImageUploadSizeTests(MediaRootMixin, TestCase):
    def oversized(self):
        upload = png_upload("big.png", side=64)  # noise does not compress: ~12 KB
        self.assertGreater(upload.size, 1024)
        return upload

    def test_validator_rejects_an_oversized_upload(self):
        with self.assertRaises(ValidationError) as caught:
            validate_image_upload_size(self.oversized())
        self.assertEqual(caught.exception.code, "file_too_large")

    def test_validator_accepts_a_small_upload_and_empty_values(self):
        validate_image_upload_size(png_upload())
        validate_image_upload_size(None)

    def test_model_rejects_an_oversized_upload(self):
        human = Human(name="Too big", image=self.oversized())
        with self.assertRaises(ValidationError) as caught:
            human.full_clean()
        self.assertIn("image", caught.exception.message_dict)

    def test_limited_form_rejects_an_oversized_upload(self):
        human = Human.objects.create(name="Owner")
        form = LimitedHumanEditForm(
            data={"name": "Owner"}, files={"image": self.oversized()}, instance=human
        )
        self.assertFalse(form.is_valid())
        self.assertIn("at most", str(form.errors["image"]))

    def test_stored_images_are_not_rechecked(self):
        with override_settings(MAX_IMAGE_UPLOAD_SIZE=10 * 1024 * 1024):
            human = Human.objects.create(name="Stored", image=png_upload())
        human = Human.objects.get(pk=human.pk)
        human.image.storage.delete(human.image.name)  # even a missing file saves
        human.name = "Stored again"
        human.save()
