class ReportService:

    def generate(self, metadata, gemma_result):

        return {
            "success": True,

            "faces_detected": metadata["faces"],

            "image_width": metadata["width"],
            "image_height": metadata["height"],

            "face_region": metadata["region"],

            "original_image": metadata["original_image"],
            "protected_image": metadata["protected_image"],

            "risk_analysis": gemma_result
        }


report_service = ReportService()