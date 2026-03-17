"""
Management command: seed_counties
Usage: python manage.py seed_counties
Seeds all 47 Kenya counties and 8 regions. Safe to run multiple times.
"""
from django.core.management.base import BaseCommand
from apps.projects.models import Region, County


REGIONS = [
    {"name": "Nairobi Metropolitan", "code": "NBI"},
    {"name": "Coast Region",          "code": "CST"},
    {"name": "Central Region",        "code": "CTR"},
    {"name": "Rift Valley Region",    "code": "RVL"},
    {"name": "Western Region",        "code": "WST"},
    {"name": "Nyanza Region",         "code": "NYZ"},
    {"name": "Eastern Region",        "code": "EST"},
    {"name": "North Eastern Region",  "code": "NET"},
]

# (county_name, county_code, region_name)
COUNTIES = [
    ("Nairobi",        "047", "Nairobi Metropolitan"),
    ("Mombasa",        "001", "Coast Region"),
    ("Kwale",          "002", "Coast Region"),
    ("Kilifi",         "003", "Coast Region"),
    ("Tana River",     "004", "Coast Region"),
    ("Lamu",           "005", "Coast Region"),
    ("Taita-Taveta",   "006", "Coast Region"),
    ("Kiambu",         "022", "Central Region"),
    ("Murang'a",       "021", "Central Region"),
    ("Kirinyaga",      "020", "Central Region"),
    ("Nyeri",          "019", "Central Region"),
    ("Nyandarua",      "018", "Central Region"),
    ("Turkana",        "023", "Rift Valley Region"),
    ("West Pokot",     "024", "Rift Valley Region"),
    ("Samburu",        "025", "Rift Valley Region"),
    ("Trans-Nzoia",    "026", "Rift Valley Region"),
    ("Uasin Gishu",    "027", "Rift Valley Region"),
    ("Elgeyo-Marakwet","028", "Rift Valley Region"),
    ("Nandi",          "029", "Rift Valley Region"),
    ("Baringo",        "030", "Rift Valley Region"),
    ("Laikipia",       "031", "Rift Valley Region"),
    ("Nakuru",         "032", "Rift Valley Region"),
    ("Narok",          "033", "Rift Valley Region"),
    ("Kajiado",        "034", "Rift Valley Region"),
    ("Kericho",        "035", "Rift Valley Region"),
    ("Bomet",          "036", "Rift Valley Region"),
    ("Kakamega",       "037", "Western Region"),
    ("Vihiga",         "038", "Western Region"),
    ("Bungoma",        "039", "Western Region"),
    ("Busia",          "040", "Western Region"),
    ("Siaya",          "041", "Nyanza Region"),
    ("Kisumu",         "042", "Nyanza Region"),
    ("Homa Bay",       "043", "Nyanza Region"),
    ("Migori",         "044", "Nyanza Region"),
    ("Kisii",          "045", "Nyanza Region"),
    ("Nyamira",        "046", "Nyanza Region"),
    ("Marsabit",       "010", "Eastern Region"),
    ("Isiolo",         "011", "Eastern Region"),
    ("Meru",           "012", "Eastern Region"),
    ("Tharaka-Nithi",  "013", "Eastern Region"),
    ("Embu",           "014", "Eastern Region"),
    ("Kitui",          "015", "Eastern Region"),
    ("Machakos",       "016", "Eastern Region"),
    ("Makueni",        "017", "Eastern Region"),
    ("Mandera",        "007", "North Eastern Region"),
    ("Wajir",          "008", "North Eastern Region"),
    ("Garissa",        "009", "North Eastern Region"),
]


class Command(BaseCommand):
    help = "Seed all 47 Kenya counties and 8 regions"

    def handle(self, *args, **options):
        self.stdout.write("Seeding regions...")
        region_map = {}
        for r in REGIONS:
            # Use name as lookup to avoid empty-code unique conflict
            obj, created = Region.objects.get_or_create(
                name=r["name"],
                defaults={"code": r["code"], "is_active": True},
            )
            # Update code if it was blank
            if not obj.code:
                obj.code = r["code"]
                obj.save(update_fields=["code"])
            region_map[r["name"]] = obj
            self.stdout.write(f"  {'created' if created else 'exists'}: {obj.name}")

        self.stdout.write("\nSeeding counties...")
        for name, code, region_name in COUNTIES:
            region_obj = region_map.get(region_name)
            obj, created = County.objects.get_or_create(
                name=name,
                defaults={"code": code, "region": region_obj, "is_active": True},
            )
            if not obj.code:
                obj.code = code
                obj.save(update_fields=["code"])
            if obj.region is None and region_obj:
                obj.region = region_obj
                obj.save(update_fields=["region"])
            self.stdout.write(f"  {'created' if created else 'exists'}: {obj.name} → {region_name}")

        self.stdout.write(self.style.SUCCESS(
            f"\n✓ Done. {Region.objects.count()} regions, {County.objects.count()} counties in DB."
        ))