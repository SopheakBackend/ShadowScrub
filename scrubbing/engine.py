import re
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
        rules = [
            ("EMPLOYEE_ID", r"\bEMP[-_]?\d{3,8}", 0.95),
            ("CREDIT_CARD", r"\b(?:\d{4}[ -]?){3}\d{4}", 0.90),
            ("AGE", r"\b\d{1,3}(?:\s*[-']?\s*years?'?\s*[-']?\s*old|\s*[-']?\s*yrs?\.?\s*old|\s*yo)", 0.75),
            ("SSN", r"\b\d{3}-\d{2}-\d{4}", 0.90),
            ("IBAN", r"\b[A-Z]{2}\d{2}[A-Z0-9]{10,30}", 0.85),
            ("IP_ADDRESS", r"\b(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d?)", 0.85),
            ("AWS_ACCESS_KEY", r"\bAKIA[0-9A-Z]{16}", 0.95),
            ("JWT", r"\beyJ[A-Za-z0-9_-]+\s*\.\s*[A-Za-z0-9_-]+\s*\.\s*[A-Za-z0-9_-]+", 0.90),
            ("TICKET_ID", r"\b(?:TKT|CASE|REQ|INC)[-_]?\d{4,10}", 0.90),
            ("PHONE_NUMBER", r"\b\+?\s*(?:1[\s-]*)?\(?\d{3}\)?[\s-]*\d{3}[\s-]*\d{4}", 0.70),
        ]

        for entity, regex, score in rules:
            pattern = Pattern(
                name=f"{entity.lower()}_pattern",
                regex=regex,
                score=score,
            )
            recognizer = PatternRecognizer(
                supported_entity=entity,
                patterns=[pattern],
                supported_language="en",
            )
            self.analyzer.registry.add_recognizer(recognizer)
        # #Employee regex
        # emp_pattern = Pattern(
        #     name="employee_id_pattern",
        #     regex=r"\bEMP[-_]?\d{3,8}\b",
        #     score=0.95
        # )
        # emp_recognizer = PatternRecognizer(
        #     supported_entity="EMPLOYEE_ID",
        #     patterns=[emp_pattern]
        # )
        # self.analyzer.registry.add_recognizer(emp_recognizer)
        
        # #Credit card regex
        # credit_card_pattern = Pattern(
        #     name="credit_card_pattern",
        #     regex = r"\b(?:\d[ -]*?){13,19}\b",
        #     score = 0.9
        # )
        # credit_card_recognizer = PatternRecognizer(
        #     supported_entity='CREDIT_CARD',
        #     patterns=[credit_card_pattern]
        # )
        # self.analyzer.registry.add_recognizer(credit_card_recognizer)
        
        # #Age pattern regex
        # age_pattern = Pattern(
        #     name='age_pattern',
        #     regex=r"\b\d{1,3}(?:\s*[-']?\s*years?'?\s*[-']?\s*old|\s*[-']?\s*yrs?\.?\s*old|\s*yo)\b",
        #     score = 0.7
        # )
        # age_recognizer = PatternRecognizer(
        #     supported_entity="AGE",
        #     patterns=[age_pattern]
        # )
        # self.analyzer.registry.add_recognizer(age_recognizer)
        
       # SSN
        # ssn_pattern = Pattern(
        #     name="ssn_pattern",
        #     regex=r"\b\d{3}-\d{2}-\d{4}\b",
        #     score=0.85
        # )
        # ssn_recognizer = PatternRecognizer(
        #     supported_entity="SSN",
        #     patterns=[ssn_pattern]
        # )
        # self.analyzer.registry.add_recognizer(ssn_recognizer)

        # # IBAN
        # iban_pattern = Pattern(
        #     name="iban_pattern",
        #     regex=r"\b[A-Z]{2}\d{2}[A-Z0-9]{10,30}\b",
        #     score=0.80
        # )
        # iban_recognizer = PatternRecognizer(
        #     supported_entity="IBAN",
        #     patterns=[iban_pattern]
        # )
        # self.analyzer.registry.add_recognizer(iban_recognizer)

        # # IP address
        # ipv4_pattern = Pattern(
        #     name="ipv4_pattern",
        #     regex=r"\b(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\b",
        #     score=0.80
        # )
        # ipv4_recognizer = PatternRecognizer(
        #     supported_entity="IP_ADDRESS",
        #     patterns=[ipv4_pattern]
        # )
        # self.analyzer.registry.add_recognizer(ipv4_recognizer)

        # # AWS access key
        # aws_key_pattern = Pattern(
        #     name="aws_key_pattern",
        #     regex=r"\bAKIA[0-9A-Z]{16}\b",
        #     score=0.95
        # )
        # aws_key_recognizer = PatternRecognizer(
        #     supported_entity="AWS_ACCESS_KEY",
        #     patterns=[aws_key_pattern]
        # )
        # self.analyzer.registry.add_recognizer(aws_key_recognizer)

        # # JWT
        # jwt_pattern = Pattern(
        #     name="jwt_pattern",
        #     regex=r"\beyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\b",
        #     score=0.90
        # )
        # jwt_recognizer = PatternRecognizer(
        #     supported_entity="JWT",
        #     patterns=[jwt_pattern]
        # )
        # self.analyzer.registry.add_recognizer(jwt_recognizer)

        # # Ticket / case / incident / request IDs
        # ticket_pattern = Pattern(
        #     name="ticket_pattern",
        #     regex=r"\b(?:TKT|CASE|REQ|INC)[-_]?\d{4,10}\b",
        #     score=0.85
        # )
        # ticket_recognizer = PatternRecognizer(
        #     supported_entity="TICKET_ID",
        #     patterns=[ticket_pattern]
        # )
        # self.analyzer.registry.add_recognizer(ticket_recognizer)
        #                                                     # -> dict here is use only for cosmetic, it means that when u call sanitize function, it will show a helper pop up that work with dict, without -> dict, thing still work just when u call sanitize, it wont show the popup helper
    def sanitize(self, text:str, active_entities:list = None) -> dict:
        """
        Scans raw text and replaces detected PII with anonimized tags or values instead.
        """
        # Keep normal newlines / original structure
        text = text.replace("\r\n", "\n").replace("\r", "\n")
        
        # Fix JWT only when PDF splits it across lines
        text = re.sub(
            r"(eyJ[A-Za-z0-9_-]+)\n([A-Za-z0-9_-]+\.[A-Za-z0-9_-]+)",
            r"\1\2",
            text,
        )
        text = re.sub(
            r"(eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+)\n([A-Za-z0-9_-]+)",
            r"\1\2",
            text,
        )
        if not active_entities:
            active_entities = [
                'PERSON',
                "PHONE_NUMBER",
                "EMAIL_ADDRESS",
                "CREDIT_CARD",
                "EMPLOYEE_ID",   
                "LOCATION",
                "AGE",
                "SSN",
                "IBAN",
                "IP_ADDRESS",
                "AWS_ACCESS_KEY",
                "JWT",
                "TICKET_ID",
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