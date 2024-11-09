from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from fastapi import Request

app = FastAPI()

# Setup for serving static files (for any CSS/JS files if needed)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates folder for HTML
templates = Jinja2Templates(directory="templates")

class CalculatorInput(BaseModel):
    num1: float
    num2: float
    operation: str

# Route to serve the main calculator page (HTML)
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "result": None})

# Route to process the calculation
@app.post("/calculate", response_class=HTMLResponse)
async def calculate(
    request: Request,
    num1: float = Form(...),
    num2: float = Form(...),
    operation: str = Form(...)
):
    result = None
    try:
        
        if operation == "add":
            result = num1 + num2
        elif operation == "subtract":
            print(num1,num2)
            result = num1 - num2
        elif operation == "divison":
            result = num1 * num2
        elif operation == "multiplication":
            result = num1 % num2  
           
            if num2 == 0:
                raise HTTPException(status_code=400, detail="Cannot divide by zero")
            result = num1 / num2
        else:
            raise HTTPException(status_code=400, detail="Invalid operation")
    
        return templates.TemplateResponse("index.html", {
            "request": request, 
            "result": result, 
            "num1": num1, 
            "num2": num2, 
            "operation": operation
        })
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


            

