from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, conlist
from typing import List
import uvicorn

app = FastAPI(title="Financial Calculator API")

# Models
class TaxInput(BaseModel):
    amount: float
    tax_rate: float  # as a percentage, e.g., 15 for 15%

class TaxOutput(BaseModel):
    tax: float
    total_amount: float

class InterestInput(BaseModel):
    principal: float
    rate: float  # annual interest rate in percentage
    time: float  # time in years
    compound: bool = False
    times_compounded: int = 1  # times per year, relevant if compound is True

class InterestOutput(BaseModel):
    interest: float
    total_amount: float

class InvoiceItem(BaseModel):
    description: str
    quantity: int
    unit_price: float

class InvoiceInput(BaseModel):
    items: List[InvoiceItem]
    tax_rate: float = 0.0  # optional tax rate
    discount: float = 0.0  # optional discount amount

class InvoiceOutput(BaseModel):
    subtotal: float
    tax: float
    discount: float
    total: float

# Endpoints
@app.post("/calculate_tax", response_model=TaxOutput)
def calculate_tax(tax_input: TaxInput):
    if tax_input.amount < 0 or tax_input.tax_rate < 0:
        raise HTTPException(status_code=400, detail="Amount and tax rate must be non-negative.")
    tax = tax_input.amount * (tax_input.tax_rate / 100)
    total = tax_input.amount + tax
    return TaxOutput(tax=round(tax, 2), total_amount=round(total, 2))

@app.post("/calculate_interest", response_model=InterestOutput)
def calculate_interest(interest_input: InterestInput):
    if interest_input.principal < 0 or interest_input.rate < 0 or interest_input.time < 0:
        raise HTTPException(status_code=400, detail="Principal, rate, and time must be non-negative.")
    rate_decimal = interest_input.rate / 100
    if interest_input.compound:
        amount = interest_input.principal * (1 + rate_decimal / interest_input.times_compounded) ** (interest_input.times_compounded * interest_input.time)
    else:
        amount = interest_input.principal * (1 + rate_decimal * interest_input.time)
    interest = amount - interest_input.principal
    return InterestOutput(interest=round(interest, 2), total_amount=round(amount, 2))

@app.post("/calculate_invoice", response_model=InvoiceOutput)
def calculate_invoice(invoice_input: InvoiceInput):
    subtotal = sum(item.quantity * item.unit_price for item in invoice_input.items)
    tax = subtotal * (invoice_input.tax_rate / 100)
    total = subtotal + tax - invoice_input.discount
    if total < 0:
        raise HTTPException(status_code=400, detail="Total amount cannot be negative.")
    return InvoiceOutput(
        subtotal=round(subtotal, 2),
        tax=round(tax, 2),
        discount=round(invoice_input.discount, 2),
        total=round(total, 2)
    )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)