# Table Generator (TG)

A comprehensive Django web application for managing World of Darkness tabletop RPG characters, items, and locations across multiple game lines.

## Overview

Table Generator is a feature-rich character management system designed for World of Darkness campaigns. It supports multiple game lines including Vampire: the Masquerade, Werewolf: the Apocalypse, Mage: the Ascension, Wraith: the Oblivion, Changeling: the Dreaming, and Demon: the Fallen.

### Key Features

- **Multi-Gameline Support** - Full character creation and management for 6+ WoD game lines
- **Chronicle Management** - Organize campaigns with storytellers, players, scenes, and stories
- **Permissions System** - Fine-grained access control for characters, items, and locations
- **XP & Freebie Tracking** - Comprehensive character progression with approval workflows
- **Character Templates** - Pre-built templates for quick character and NPC creation
- **Polymorphic Models** - Flexible inheritance system for game-specific features
- **Responsive UI** - Custom-designed interface with gameline-specific theming

## Quick Start

### Prerequisites

- Python 3.10+
- pip and virtualenv
- Git

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/tg.git
cd tg

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
# Create .env file with your configuration
cp .env.example .env
# Edit .env with your SECRET_KEY and other settings

# Run migrations
python manage.py migrate

# Load game data
bash setup_db.sh

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic

# Run development server
python manage.py runserver
```

Visit `http://localhost:8000` to access the application.

### Secrets Configuration

You'll need to create a `.env` file with your configuration:

```bash
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
```

Generate a secure secret key:
```python
import secrets
print(secrets.token_urlsafe(50))
```

## Project Structure

```
tg/
├── characters/        # Character models, views, forms by gameline
├── items/             # Equipment and artifacts
├── locations/         # Places and locations
├── game/              # Chronicle, Scene, Story management
├── accounts/          # User profiles and authentication
├── core/              # Shared utilities, base models, permissions
├── populate_db/       # Game data loading scripts
├── docs/              # Documentation
│   ├── design/        # Design specifications
│   ├── guides/        # Implementation guides
│   ├── deployment/    # Deployment documentation
│   └── testing/       # Test documentation
└── static/            # CSS, JavaScript, images
```

## Documentation

### For Developers

- **[CLAUDE.md](CLAUDE.md)** - Comprehensive development guide for working with this codebase
- **[docs/guides/](docs/guides/)** - Implementation guides for specific features
- **[docs/design/](docs/design/)** - Design documentation and specifications
- **[TODO.md](TODO.md)** - Known issues and planned improvements

### For Deployment

- **[docs/deployment/](docs/deployment/)** - Complete deployment guides for staging and production
- Includes permissions system and validation system deployment documentation

### Key Documentation

- **Permissions System** - [docs/design/permissions_system.md](docs/design/permissions_system.md)
- **Data Validation** - [docs/design/data_validation.md](docs/design/data_validation.md)
- **Limited Forms** - [docs/guides/limited_owner_forms.md](docs/guides/limited_owner_forms.md)
- **View Migration** - [docs/guides/view_template_migration.md](docs/guides/view_template_migration.md)

## Technology Stack

- **Backend**: Django 5.1.7
- **Database**: SQLite (development) / PostgreSQL (production)
- **ORM**: Django ORM with django-polymorphic for inheritance
- **Frontend**: Bootstrap 5 with custom TG styling
- **Testing**: Django's unittest framework
- **Dependencies**: See [requirements.txt](requirements.txt)

## Game Lines Supported

- **World of Darkness** (WoD) - Core system
- **Vampire: the Masquerade** (VtM) - Clans, disciplines, blood bonds
- **Werewolf: the Apocalypse** (WtA) - Tribes, gifts, renown
- **Mage: the Ascension** (MtA) - Traditions, spheres, arete
- **Wraith: the Oblivion** (WtO) - Passions, fetters, shadow
- **Changeling: the Dreaming** (CtD) - Kiths, arts, glamour
- **Demon: the Fallen** (DtF) - Houses, lores, torment

## Testing

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test characters

# Run with verbose output
python manage.py test --verbosity=2

# Run specific test class
python manage.py test characters.tests.core.test_permissions.TestOwnerPermissions

# Run specific test method
python manage.py test characters.tests.core.test_permissions.TestOwnerPermissions.test_owner_can_view_full
```

## Contributing

1. Create a feature branch from `main`
2. Make your changes
3. Write/update tests
4. Update documentation
5. Submit a pull request

### Code Style

- Follow Django best practices
- Use Black for Python formatting
- Follow patterns documented in CLAUDE.md
- Write tests for new features
- Update documentation

## Common Commands

```bash
# Database
python manage.py makemigrations
python manage.py migrate
python manage.py dbshell

# Development
python manage.py runserver
python manage.py shell
python manage.py createsuperuser

# Testing
python manage.py test                     # All tests
python manage.py test characters          # App-specific tests
python manage.py test --verbosity=2       # Verbose output

# Data Management
bash setup_db.sh                          # Load all game data
python manage.py loaddata <fixture>       # Load specific fixture

# Deployment
python manage.py collectstatic
python manage.py check --deploy
```

## Architecture Highlights

### Polymorphic Models

The application uses django-polymorphic for flexible model inheritance:

```python
# Base model
Character (polymorphic)
├── Human
│   ├── VtMHuman (Vampire character)
│   ├── Garou (Werewolf character)
│   └── Mage (Mage character)
└── Spirit
    └── Wraith
```

### Permissions System

Fine-grained permissions control access to objects:

- **VIEW_FULL** - See all character details
- **VIEW_PARTIAL** - See limited public information
- **EDIT_FULL** - Modify all fields (ST/Admin only)
- **EDIT_LIMITED** - Modify notes and descriptions (Owner)
- **SPEND_XP** - Use experience points
- **APPROVE** - Approve character changes (ST only)

See [docs/design/permissions_system.md](docs/design/permissions_system.md) for details.

### Chronicle System

Campaigns are organized through Chronicles:

- **Chronicle** - The campaign container
- **Story** - Multi-session story arcs
- **Scene** - Individual game sessions
- **Week** - Weekly time tracking for XP awards

## License

[Add your license information here]

## Support

For issues and questions:
- Create an issue in the issue tracker
- Review existing documentation in `docs/`
- Check `TODO.md` for known issues

## Credits

Built with Django and love for World of Darkness.

---

**Version**: 2.0
**Django**: 5.1.7
**Python**: 3.10+
