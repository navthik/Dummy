import pandas as pd
import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv(override=True)

class GeminiCSVAgent:
    def __init__(self, csv_path):
        """Initialize Gemini-powered CSV/Excel agent with direct API usage."""
        self.api_key = self.configure_gemini()
        self.df = self.load_data(csv_path)

    def configure_gemini(self):
        """Configure Gemini with API Key."""
        api_key = os.getenv("GOOGLE_API_KEY")
        print(f"API Key: {api_key}")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY missing in .env file. Please add it.")
        genai.configure(api_key=api_key)
        return api_key

    def load_data(self, path):
        """Load CSV or Excel file."""
        if not os.path.exists(path):
            raise FileNotFoundError(f"❌ File not found: {path}")

        try:
            if path.endswith('.csv'):
                return pd.read_csv(path, encoding='utf-8')
            elif path.endswith('.xlsx') or path.endswith('.xls'):
                return pd.read_excel(path)
            else:
                raise ValueError("❌ Only CSV or Excel files supported.")
        except Exception as e:
            raise ValueError(f"❌ Error loading file: {str(e)}")

    def get_data_context(self):
        """Get columns and sample data."""
        return (
            list(self.df.columns),
            self.df.head(3).to_markdown(index=False)
        )

    def query_gemini(self, prompt_text):
        """Send a prompt to Gemini and return the result."""
        model = genai.GenerativeModel(model="gemini-pro")  # Adjust model initialization
        response = model.generate_content(prompt_text)
        return response.text


    def execute_query(self, query):
        """Process user query."""
        query = query.lower().strip()

        if "top" in query and ("customer" in query or "purchase" in query):
            return self.top_customers()
        elif "how many" in query and "bought" in query:
            return self.handle_product_query(query, self.count_product_customers)
        elif "list all products" in query or "list products purchased" in query:
            return self.handle_customer_query(query, self.get_customer_products)
        elif "who purchased" in query:
            return self.handle_product_query(query, self.get_product_customers)
        elif "unique products" in query or "total unique products" in query:
            return self.unique_products_count()
        else:
            return self.analyze_with_gemini(query)

    def handle_product_query(self, query, func):
        """Extract product and call function."""
        try:
            product = query.split("[")[1].split("]")[0].strip()
            return func(product)
        except IndexError:
            return "⚠️ Please specify product inside brackets like [Product Name]"

    def handle_customer_query(self, query, func):
        """Extract customer and call function."""
        try:
            customer = query.split("[")[1].split("]")[0].strip()
            return func(customer)
        except IndexError:
            return "⚠️ Please specify customer inside brackets like [Customer Name]"

    def top_customers(self):
        """Top 5 customers by purchase_count."""
        if 'purchase_count' not in self.df.columns:
            return "⚠️ 'purchase_count' column not found."
        top = self.df.nlargest(5, 'purchase_count')
        return top[['customer_name', 'purchase_count']].to_markdown(index=False)

    def count_product_customers(self, product):
        """Count customers for a product."""
        if 'product_name' not in self.df.columns or 'customer_name' not in self.df.columns:
            return "⚠️ Required columns missing."
        count = self.df[self.df['product_name'].str.lower() == product.lower()]['customer_name'].nunique()
        return str(count)

    def get_customer_products(self, customer):
        """List products bought by a customer."""
        if 'customer_name' not in self.df.columns or 'product_name' not in self.df.columns:
            return "⚠️ Required columns missing."
        products = self.df[self.df['customer_name'].str.lower() == customer.lower()]['product_name'].unique()
        return ", ".join(products) if products.size > 0 else "No products found."

    def get_product_customers(self, product):
        """List customers who bought a product."""
        if 'customer_name' not in self.df.columns or 'product_name' not in self.df.columns:
            return "⚠️ Required columns missing."
        customers = self.df[self.df['product_name'].str.lower() == product.lower()]['customer_name'].unique()
        return ", ".join(customers) if customers.size > 0 else "No customers found."

    def unique_products_count(self):
        """Unique products count."""
        if 'product_name' not in self.df.columns:
            return "⚠️ 'product_name' column missing."
        return str(self.df['product_name'].nunique())

    def analyze_with_gemini(self, query):
        """Use Gemini for complex analysis."""
        columns, sample = self.get_data_context()
        prompt = f"""
You are a professional data analyst.
Available columns: {columns}
Sample Data:
{sample}

Instruction: {query}
Only give precise factual answers, no unnecessary details.
"""
        try:
            return self.query_gemini(prompt)
        except Exception as e:
            return f"❌ Gemini error: {str(e)}"


# Usage example
if __name__ == "__main__":
    try:
        agent = GeminiCSVAgent(r"C:\Users\Navthik_rk\OneDrive\Videos\AI Agent\data\dummy_myntra (2).xlsx")
        queries = [
            "Show top 5 customers by purchases",
            "How many customers bought [Wireless Mouse]?",
            "List products purchased by [John Doe]",
            "Customers who purchased [USB-C Hub]",
            "Total unique products?",
            "Analyze purchase patterns between different product categories"
        ]

        for q in queries:
            print(f"\n🔍 Query: {q}")
            print(f"📝 Response:\n{agent.execute_query(q)}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
