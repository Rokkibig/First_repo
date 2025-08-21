class DummyWorkflow:
    async def ainvoke(self, state):
        return {
            "delivery_status": "ready",
            "final_response": {"results": "contract_analysis"}
        }

def build_legal_workflow():
    return DummyWorkflow()
