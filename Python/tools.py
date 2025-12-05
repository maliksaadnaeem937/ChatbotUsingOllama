from langchain.tools import tool
from langchain_core.output_parsers import StrOutputParser
from datetime import date
from backend import llm
from models import ExpenseInput

# Define categories
CATEGORIES = [
    "Food",
    "Transport",
    "Entertainment",
    "Bills",
    "Shopping",
    "Health",
    "Education",
    "Others"
]

# Initialize in-memory database (you should replace this with a real database)
expenses_db = []


@tool("CategorizeExpense", return_direct=False)
def categorize_expense(title: str, description: str = "") -> str:
    """
    Ask the LLM to classify the expense into one of the predefined categories.
    
    Args:
        title (str): Short description of the expense.
        description (str, optional): Additional details.
    
    Returns:
        str: Category chosen from the predefined list.
    """
    prompt = f"""
    You are given an expense with the following information:
    Title: {title}
    Description: {description}

    Choose the most appropriate category from this list: {', '.join(CATEGORIES)}.
    Respond only with the category name.
    """
    
    response = llm.predict(prompt)
    category = response.strip()
    
    # Validate category
    if category not in CATEGORIES:
        return "Others"
    
    return category


@tool("AddExpense", return_direct=True)
def add_expense(title: str, amount: float, category: str = None, expense_date: str = None, description: str = "") -> str:
    """
    Adds a new expense to the database.

    Args:
        title (str): Short description of the expense
        amount (float): Money spent
        category (str, optional): e.g., Food, Transport, Bills; auto-selected if missing
        expense_date (str, optional): Date of expense in YYYY-MM-DD format; defaults to today
        description (str, optional): Extra notes
    
    Returns:
        str: Confirmation message
    """
    # Fill defaults
    if category is None or category not in CATEGORIES:
        category = categorize_expense(title, description)
    
    if expense_date is None:
        expense_date = date.today()
    else:
        # Parse date string if provided
        try:
            expense_date = date.fromisoformat(expense_date)
        except (ValueError, TypeError):
            expense_date = date.today()
    
    # Create expense object
    expense = {
        "title": title,
        "amount": amount,
        "category": category,
        "date": expense_date,
        "description": description
    }
    
    # Add to database
    expenses_db.append(expense)
    
    return f"✅ Expense '{title}' of ${amount:.2f} added under category '{category}' on {expense_date}"


# Optional: Additional helper tools

@tool("GetExpenses", return_direct=True)
def get_expenses(category: str = None) -> str:
    """
    Retrieve all expenses, optionally filtered by category.
    
    Args:
        category (str, optional): Filter by this category
    
    Returns:
        str: List of expenses
    """
    if not expenses_db:
        return "No expenses recorded yet."
    
    filtered = expenses_db
    if category and category in CATEGORIES:
        filtered = [e for e in expenses_db if e["category"] == category]
    
    if not filtered:
        return f"No expenses found{' for category ' + category if category else ''}."
    
    result = []
    total = 0
    for exp in filtered:
        result.append(f"- {exp['title']}: ${exp['amount']:.2f} ({exp['category']}) on {exp['date']}")
        total += exp['amount']
    
    return "\n".join(result) + f"\n\nTotal: ${total:.2f}"

