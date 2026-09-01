import pytest

class DocumentPipelineSimulator:
    def process_document(self, doc_name, content_type="pdf", corrupt=False, has_table=False):
        if corrupt:
            raise ValueError("ExtractionFailed: Unsupported or corrupted file stream.")
        
        stages = {
            "upload": "SUCCESS",
            "extraction": "PARTIAL" if has_table else "SUCCESS",
            "chunking": "SUCCESS",
            "indexing": "SUCCESS",
            "retrieval": "SUCCESS",
            "answer_generation": "SUCCESS"
        }
        return stages

def test_document_pipeline_success():
    pipeline = DocumentPipelineSimulator()
    result = pipeline.process_document("enterprise_policy_2026_v4.2.pdf")
    assert result["upload"] == "SUCCESS"
    assert result["extraction"] == "SUCCESS"
    assert result["indexing"] == "SUCCESS"

def test_document_processing_failure_isolation():
    pipeline = DocumentPipelineSimulator()
    with pytest.raises(ValueError, match="ExtractionFailed"):
        pipeline.process_document("corrupted_file.pdf", corrupt=True)

def test_tabular_data_partial_extraction_defect():
    """Isolates a defect where structured tables lose row-column mappings during text extraction."""
    pipeline = DocumentPipelineSimulator()
    result = pipeline.process_document("infrastructure_specs_table.pdf", has_table=True)
    # Defect isolation check: extraction flagged as PARTIAL
    assert result["extraction"] == "PARTIAL"