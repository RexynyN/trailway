import utils.printer as pr 
from utils.canonical import Canonical 
from utils.exceptions import ConfigException 
from core.step import Step 

class Journey:
    def __init__(self, inputs: dict, mapping: str, credential: str, DEBUG: bool=False) -> None:
        canon = Canonical()
        self.DEBUG = DEBUG 
        self.inputs = inputs
        self.mapping = canon.mappings(mapping=mapping)
        self.credentials = canon.credentials(credential=credential)
        if not self.mapping:
            raise ConfigException(f"O mapping '{mapping} não existe!'")
        
        if not self.credentials and credential:
            pr.warning("Nenhuma credencial encontrada, mas continuando!")

        
        self.globals = {
            **self.inputs,
            **self.credentials 
        }
        self.steps: list[Step] = []

    def run_steps(self):
        for step_args in self.mapping:
            step = Step(step_args, globals=self.globals)
            self.steps.append(step)
            self._run_step(step)

    def get_current_stats(self):
        """ Get current step stats """
        return self.steps[-1].get_stats()
        
    def get_steps_stats(self):
        """ Get all steps stats """
        return [step.get_stats() for step in self.steps]

    def get_steps_output(self):
        output = { }
        for step in self.steps:
            output = { **output, **step.get_outputs() }

        return output 
    
    def _run_step(self, step: Step):
        step.run()
        self._update_globals(step.get_arguments())

    def _update_globals(self, new_globals: dict):
        # new_globals will overwrite any existing keys with same name
        self.globals = { **self.globals, **new_globals}

    def _debug_print(self):
        if self.DEBUG:
            print("Você está em modo DEBUG")

        print("Você não está em modo DEBUG")
