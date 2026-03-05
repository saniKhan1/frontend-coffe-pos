"""Sphinx configuration for Philo Coffee Shop POS API documentation."""

project = "Philo Coffee Shop POS API"
copyright = "2026, Philo Coffee Shop"
author = "Philo Coffee Shop Team"
release = "1.0.0"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
    "sphinx.ext.napoleon",
    "sphinx_copybutton",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

html_theme = "pydata_sphinx_theme"
html_static_path = ["_static"]
html_title = "Philo Coffee Shop POS API"

# PyData theme options (pandas-style)
html_theme_options = {
    "logo": {
        "text": "Philo Coffee Shop POS",
    },
    "github_url": "https://github.com/mrqadeer/philo-coffee-shop",
    "navbar_end": ["navbar-icon-links"],
    "navbar_align": "content",
    "show_nav_level": 2,
    "navigation_depth": 4,
    "show_toc_level": 2,
    "collapse_navigation": False,
    "navigation_with_keys": True,
    "show_prev_next": True,
    "footer_start": ["copyright"],
    "footer_end": ["sphinx-version"],
    "secondary_sidebar_items": ["page-toc", "edit-this-page"],
    "use_edit_page_button": False,
}

# Copy button configuration
copybutton_prompt_text = r">>> |\.\.\. |\$ |❯ "
copybutton_prompt_is_regexp = True

# Napoleon settings for Google-style docstrings
napoleon_google_docstrings = True
napoleon_numpy_docstrings = False
napoleon_include_init_with_doc = True
