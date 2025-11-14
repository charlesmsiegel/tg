# Derangement Descriptions for World of Darkness
# This file adds descriptions to derangements defined in derangements.py
# Information extracted from Werewolf: The Apocalypse 20th Anniversary Edition and other sources

from characters.models.core.derangement import Derangement

# Create a helper function for derangements that might not exist
def set_derangement_description(name, description):
    try:
        derangement = Derangement.objects.get(name=name)
        derangement.description = description
        derangement.save()
        return True
    except Derangement.DoesNotExist:
        print(f"Derangement '{name}' not found, skipping...")
        return False

# Derangements

set_derangement_description("Fugue", """Also known as dissociative fugue, this severe derangement causes the character to experience periods of time where they lose awareness of their identity and may travel to unfamiliar places with no memory of how they got there or what they did. During a fugue state, the character may adopt a different personality or identity entirely, acting on impulses and desires they would normally suppress.

Fugue episodes are typically triggered by extreme stress or trauma. The character "wakes up" hours, days, or even weeks later with no memory of what transpired. They may find themselves in strange locations, discover evidence of actions they don't remember taking, or learn from others about behaviors completely unlike their normal personality.

System: When the character experiences overwhelming stress (Storyteller's discretion), they must roll Willpower (difficulty 8). Failure means they enter a fugue state. During the fugue, the Storyteller controls the character, who acts on subconscious desires and impulses. When the character emerges from the fugue, they have no memory of their actions. The fugue typically lasts until the stress that triggered it is resolved or escaped, though it could persist for days or longer in severe cases.""")

set_derangement_description("Hysteria", """This derangement manifests as uncontrolled emotional outbursts triggered by stress or specific stimuli. The hysterical character experiences overwhelming emotions that they cannot regulate - sudden sobbing, uncontrollable laughter, screaming, or other extreme emotional responses that are disproportionate to the situation.

Hysteria represents a complete failure of emotional regulation. The character knows their reaction is excessive but cannot stop themselves. These episodes are exhausting and humiliating, but the character is helpless to prevent them when triggered.

System: When faced with stress or the specific trigger for their hysteria (Storyteller's discretion), the character must make a Willpower roll (difficulty 7). Failure means they dissolve into an uncontrollable emotional outburst that lasts for a full scene. During this time, they cannot take rational action and may draw unwanted attention. Some forms of hysteria may also manifest physical symptoms like temporary blindness, paralysis, or seizures - these are psychological in origin but very real in effect. The character is incapacitated for the duration.""")

set_derangement_description("Multiple Personalities", """Also known as Dissociative Identity Disorder, this severe derangement causes the character's psyche to fragment into multiple distinct personalities, each with their own memories, behaviors, and traits. These alternate personalities (alters) emerge in response to stress, taking control of the body while the primary personality becomes dormant.

Each personality may be unaware of the others, leading to lost time and confusion when one personality recedes and another emerges. Different alters may have different Abilities, Virtues, Willpower, or even Nature and Demeanor. Some alters may be protectors, others may be aggressive, and some may even be supernatural in cases where the character has been through transformative trauma.

System: The character has 2-4 distinct personalities (Storyteller determines exact number and nature). When stressed, the character must roll Willpower (difficulty 8). Failure means a different personality emerges to deal with the situation. The Storyteller should create personality profiles for each alter, possibly with different trait ratings. Switching between personalities causes the character to lose consciousness briefly (a few seconds to a few minutes). Personalities may leave notes or messages for each other, or they may be completely unaware of each other's existence. Achieving awareness and cooperation between alters requires extensive therapy and is difficult even for supernatural beings.""")

set_derangement_description("Obsessive-Compulsive", """This derangement manifests as intrusive, unwanted thoughts (obsessions) and repetitive behaviors or mental acts (compulsions) that the character feels driven to perform. Common obsessions include fear of contamination, need for symmetry, or intrusive violent or blasphemous thoughts. Common compulsions include excessive handwashing, counting, checking locks repeatedly, or arranging objects in specific patterns.

The character recognizes these thoughts and behaviors are irrational but cannot stop them. Failing to perform their compulsions when stressed causes intense anxiety. The compulsions provide temporary relief but don't address the underlying anxiety, creating a self-perpetuating cycle.

System: The character has specific obsessions and compulsions (player and Storyteller determine these). When stressed or confronted with triggers for their obsession, the character must make a Willpower roll (difficulty 7). Failure means they must perform their compulsion immediately, even if doing so is dangerous or inappropriate. The compulsion takes at least a few minutes (or longer for complex rituals) and the character cannot focus on other tasks until it's completed. Resisting a compulsion through successful Willpower roll causes the character to suffer a +1 difficulty to all actions for the next scene due to anxiety.""")

set_derangement_description("Paranoia", """The paranoid character believes that others are conspiring against them, watching them, or plotting their downfall. While supernatural beings often have genuine enemies, paranoia goes beyond justified caution into delusional territory. The paranoid individual sees threats where none exist, interprets neutral actions as hostile, and trusts no one.

Paranoia makes cooperation and social interaction extremely difficult. The character may refuse to eat food prepared by others (fearing poison), avoid going certain places (believing ambushes await), or betray allies (convinced they were about to betray first).

System: The character must make a Willpower roll (difficulty 7) when presented with evidence that could be interpreted as threatening, even if innocent explanations exist. Failure means the character interprets the situation in the most paranoid possible way and acts accordingly. The character suffers +2 difficulty to all Social rolls due to their obvious suspicion and inability to trust. On the positive side, paranoid characters are genuinely harder to ambush or deceive - they get -1 difficulty on rolls to detect actual threats or lies, as their hypervigilance sometimes pays off.""")

set_derangement_description("Schizophrenia", """This severe derangement involves a disconnection from reality, manifesting as hallucinations (perceiving things that aren't there), delusions (firmly held false beliefs), disorganized thinking, and inappropriate emotional responses. The schizophrenic character may hear voices, see visions, believe they are receiving messages from higher powers, or construct elaborate delusional frameworks that don't align with reality.

For supernatural beings, schizophrenia is particularly insidious because they DO experience things beyond normal reality. Distinguishing between genuine supernatural perception and hallucination becomes nearly impossible.

System: The character experiences hallucinations and delusions regularly. The Storyteller should occasionally provide false sensory information, secret messages that don't exist, or convince the character that something happening is actually something else. The character must make Willpower rolls (difficulty 8) to distinguish reality from delusion, with failure meaning they cannot tell the difference. Schizophrenic characters suffer +2 difficulty to all Mental and Social rolls due to their disorganized thinking and inappropriate responses. In combat or crisis situations, they may freeze up, respond to threats that aren't there, or ignore real dangers in favor of delusional priorities. Medication can help manage symptoms but often dulls supernatural perceptions as well, forcing difficult choices.""")

print("Derangement descriptions have been added successfully!")
