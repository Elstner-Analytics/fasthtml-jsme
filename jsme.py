from fasthtml.common import * 

jsme = Script(src="assets/jsme/jsme.nocache.js")
jsmestyle = Link(rel="stylesheet", href="assets/jsme/bootstrap.css", type="text/css")

jsme_script = """
function jsmeOnLoad() {
    jsmeApplet = new JSApplet.JSME("jsme_container", "600px", "400px");
}

htmx.on("htmx:configRequest", (event) => {
    let smiles = jsmeApplet.smiles();
    event.detail.parameters['smiles'] = smiles;
});
"""

app, rt = fast_app(hdrs=(jsme,jsmestyle))

# For images, CSS, etc.
@app.get("/{fname:path}.{ext:static}")
def static(fname:str, ext:str): return FileResponse(f'{fname}.{ext}')

@rt("/")
def get():
    return Titled("Chemical World", 
        Div(id="jsme_container", style="width: 600px; height: 400px;"),
        P(),
        Button("Submit SMILES", 
               hx_post="/submit_smiles", 
               hx_trigger="click",
               hx_target="#results"),
        Div(id="results"),
        Script(jsme_script)
                  )

@rt("/submit_smiles")
def post(smiles:str):
    return Div(f"SMILES: {smiles}", id="results")

serve()