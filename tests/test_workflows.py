import asyncio
from workflows.graph_builder import build_legal_workflow

def test_contract_analysis_workflow():
    workflow = build_legal_workflow()
    test_state = {
        'request_id': 'test_123',
        'request_type': 'contract_review',
        'input_documents': [{'type': 'contract', 'content': '...'}],
        'query': 'Review this contract for risks',
        'context': {'jurisdiction': 'NY'}
    }
    result = asyncio.run(workflow.ainvoke(test_state))
    assert result['delivery_status'] == 'ready'
    assert 'contract_analysis' in result['final_response']['results']
