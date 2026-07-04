from app.protection.pipeline import process_image


class ProtectionService:

    def apply_protection(self, input_path: str):
        """
        Executes the complete protection pipeline.
        """
        return process_image(input_path)


protection_service = ProtectionService()