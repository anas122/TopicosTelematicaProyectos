import pickle

from urllib.parse import urlparse 
from urllib.parse import parse_qs

from constants import filename, port, address

import http.server

import ray


class HTTPRQH(http.server.BaseHTTPRequestHandler):
    base = {}

    ray.init(address='auto')
    
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_HEAD(self):
        self._set_headers()
    
    def do_POST(self):
        self._set_headers()
        future = load.remote()
        self.base = ray.get(future)
        if(self.command == 'POST'):
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            post_data = post_data.decode('utf-8')
            key = post_data[0]
            value = post_data[2:]
            print(value)
            if key in self.base:
                self.base[key].append(value)
                save.remote(self.base)
            else:
                self.base[key]=[value]
                save.remote(self.base)
        else: 
            self.send_response(404) 
    
    def do_GET(self):
        self._set_headers()
        future = load.remote()
        self.base = ray.get(future)
        if(self.command == 'GET'):
            parsed_url = urlparse(self.path)
            key = parse_qs(parsed_url.query).get("key")[0]
            print(key)
            if key in self.base :
                value = self.base.get(key)
                self.wfile.write(bytes("<html><body>"+ value[len(value)-1] +"</body></html>",'utf-8'))
                print("Existe la llave y este es el último valor " + value[len(value)-1])
            else:
                self.wfile.write(bytes("<html><body><p>No existe la llave buscada</p></body></html>",'utf-8'))
                print("No existe")
        else:
            self.send_response(404)

    def do_DELETE(self):
        self._set_headers()
        future = load.remote()
        self.base = ray.get(future)
        if(self.command == 'DELETE'):
            parsed_url = urlparse(self.path)
            key = parse_qs(parsed_url.query).get("key")[0]
            if key in self.base:
                self.base.pop(key)
                self.wfile.write(bytes("<html><body><p> Se ha eliminado el objeto :"+ key +"</p></body></html>",'utf-8'))
                save.remote(self.base)
            else:
                self.wfile.write(bytes("<html><body><p>No existe la llave buscada</p></body></html>",'utf-8')) 
        else:
            self.send_response(404)


@ray.remote
def save(base):
        with open(filename,'wb') as f:
            pickle.dump(base, f)

@ray.remote
def load():
    base = {}
    with open(filename,'rb') as f:
        base = pickle.load(f)
    return base    

def main():
    Handler = HTTPRQH
    with http.server.HTTPServer((address, port), Handler) as httpd:
        print("serving at port", port)
        httpd.serve_forever()


main()

