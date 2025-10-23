import requests 
import utils.requestutils as ru 
import warnings
from utils.exceptions import RequestException, StepException
from requests.exceptions import HTTPError


class Request:
    def __init__(self, url: str, headers: dict, payload: dict, name: str, verb: str, tls: bool, status: list) -> None:
        self.name = name 
        self.url = url 
        self.verb = verb 
        self.headers = headers
        self.payload = payload 
        self.response = { }
        self.url_parts = []
        self.status = status 
        self.stats = {}
        self.tls = tls 

    def request(self, strict: bool=False) -> None:
        """
        Makes the specified request and gets the response 
        
        strict: When validating the url makes sure that extra url parts aren't present
        """

        if not self._validate_url(strict=strict):
            raise RequestException(ru.error_message(self.url_parts))
        
        try:
            with warnings.catch_warnings():
                # Suppress "unsafe request" warning as we need to unverify TLS for the request to go through
                warnings.simplefilter('ignore')
                # Check the payload to see if it is a JSON
                response = None 
                if isinstance(self.payload, dict):
                    response = requests.request(self.verb, self.url, json=self.payload, headers=self.headers, verify=self.tls)
                else:
                    response = requests.request(self.verb, self.url, data=self.payload, headers=self.headers, verify=self.tls)
                
                # Will raise exceptions if anything goes wrong (401, 404, etc...)
                self.raise_for_status(response)
                self.response = response.json()
                self._build_stats(response)
        except HTTPError as e:
            self._build_stats(response)
            raise StepException(f"Houve um erro na requisição:\n {e}", name=self.name)
        except Exception as e: 
            if response: 
                self._build_stats(response)
            raise StepException(f"Houve um erro na requisição:\n {e}", name=self.name)
    
    def raise_for_status(self, resp: requests.Response):
        # If a "good" HTTP code is passed, we make it a "Bad" HTTP code
        ok_codes = [code for code in self.status if code >= 100 and code < 400]
        if resp.status_code in ok_codes:
            raise HTTPError(f"Induzindo erro no status {resp.status_code} pelo Trail. Resposta: {resp.reason}")
        
    def _build_stats(self, response: requests.Response) -> dict:
        try: 
            self.stats['name'] = self.name
            self.stats['payload'] = self.payload
            self.stats['verb'] = self.verb
            self.stats['status_code'] = response.status_code
            self.stats['time_elapsed'] = str(response.elapsed)
            self.stats['url'] = response.url
            self.stats['request_headers'] = self.headers
            self.stats['response_header'] = dict(response.headers)
            self.stats['response'] = response.json()

        except AttributeError:
            self.stats['name'] = self.name
            self.stats['payload'] = self.payload
            self.stats['verb'] = self.verb
            self.stats['url'] = response.url
            self.stats['request_headers'] = self.headers
        
        return self.stats
    

    def _validate_url(self, strict: bool=False) -> bool:
        return ru.url_valid(self, self.url, self.url_parts, strict=strict)
    
    def _response_ok(self, code: int) -> bool:
        return (code % 200) < 100 # Check if the response code is a 2xx

    def return_response(self) -> dict: 
        return self.response
    
    def return_arguments(self, jsonpaths: list[str]) -> list:
        try:
            return ru.jsonpath_matches(self.response, jsonpaths)
        except Exception:
            raise StepException("A expressão JsonPath está incorreta!", self.name)

    def set_url(self, url: str) -> None:
        self.url = url 

    def set_urlparts(self, url_parts: list[str]) -> None:
        self.url_parts = url_parts 

    def set_headers(self, headers: str) -> None:
            self.header = headers 

    def set_payload(self, payload: dict) -> None:
            self.payload = payload

   