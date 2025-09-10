# tests/test_commands.py
from io import StringIO
from django.core.management import call_command
from django.test import TestCase

class CommandTests(TestCase):
    def test_seed_dry_run(self):
        out = StringIO()
        call_command("seed", "--dry-run", stdout=out)
        self.assertIn("Dry-run", out.getvalue())


