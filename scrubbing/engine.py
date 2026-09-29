from presidio_analyzer import AnalyzerEngine, PatternRecognizer, Pattern
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import OperatorConfig
from presidio_analyzer.nlp_engine import NlpEngineProvider

class ShadowScrubEngine:
    def __init__(self):
        configuration = {
        "nlp_engine_name": "spacy",
        "models": [{"lang_code": "en", "model_name": "en_core_web_lg"}]
        }
        provider = NlpEngineProvider(nlp_configuration=configuration)
        nlp_engine = provider.create_engine()
        
        
        self.analyzer = AnalyzerEngine(nlp_engine=nlp_engine)
        self.anonymizer = AnonymizerEngine()
        
        self.register_custom_recognizers()
    
    def register_custom_recognizers(self):
        emp_pattern = Pattern(
            name="employee_id_pattern",
            regex=r"\bEMP-\d{4}\b", 
            score=0.95
        )
        emp_recognizer = PatternRecognizer(
            supported_entity="EMPLOYEE_ID",
            patterns=[emp_pattern]
        )
        self.analyzer.registry.add_recognizer(emp_recognizer)
        
        
        credit_card_pattern = Pattern(
            name="credit_card_pattern",
            regex = r"\b(?:\d[ -]*?){13,19}\b",
            score = 0.9
        )
        credit_card_recognizer = PatternRecognizer(
            supported_entity='CREDIT_CARD',
            patterns=[credit_card_pattern]
        )
        self.analyzer.registry.add_recognizer(credit_card_recognizer)
        
        age_pattern = Pattern(
            name='age_pattern',
            regex=r"\b\d{1,3}(?:\s*[-']?\s*years?'?\s*[-']?\s*old|\s*[-']?\s*yrs?\.?\s*old|\s*yo)\b",
            score = 0.7
        )
        age_recognizer = PatternRecognizer(
            supported_entity="AGE",
            patterns=[age_pattern]
        )
        self.analyzer.registry.add_recognizer(age_recognizer)
                                                            # -> dict here is use only for cosmetic, it means that when u call sanitize function, it will show a helper pop up that work with dict, without -> dict, thing still work just when u call sanitize, it wont show the popup helper
    def sanitize(self, text:str, active_entities:list = None) -> dict:
        """
        Scans raw text and replaces detected PII with anonimized tags or values instead.
        """
        if not active_entities:
            active_entities = [
                'PERSON',
                "PHONE_NUMBER",
                "EMAIL_ADDRESS",
                "CREDIT_CARD",
                "EMPLOYEE_ID",   
                "LOCATION",
                "AGE",
            ]
        results = self.analyzer.analyze(
            text= text,
            entities= active_entities,
            language="en"
        )
        anonymized_result = self.anonymizer.anonymize(
            text= text,
            analyzer_results= results,
            operators= {
                'DEFAULT': OperatorConfig("replace", {"new_value": '[REDACTED]'})
            }   
        )
        detected_summary = {}
        for res in results:
            entity_type = res.entity_type
            detected_summary[entity_type] = detected_summary.get(entity_type, 0) + 1
        return {
            'clean_result' : anonymized_result.text,
            'detected_summary': detected_summary,
            'total_detected': len(results)
        }
        
#test script
# if __name__ == "__main__":
#     scrubber = ShadowScrubEngine()
    
#     sample_input = (
#         "Hi, my name is Sarah Connor. Call me at 555-123-4567 or email "
#         "sarah@sky.net. My internal ID is EMP-8821 and card is 4111-2222-3333-4444."
#     )
    
#     output = scrubber.sanitize(sample_input)
    
#     print("\n--- ORIGINAL TEXT ---")
#     print(sample_input)
#     print("\n--- SANITIZED TEXT ---")
#     print(output["clean_result"])
#     print("\n--- DETECTION SUMMARY ---")
#     print(output["detected_summary"])