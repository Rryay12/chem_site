from flask import Flask, render_template, request
import reaction

app = Flask(__name__)
python_reaction = reaction.reaction()

@app.route("/", methods=["GET", "POST"])
def index():
    # Initialize reaction with empty reactants, products, and a default k value
    reaction_data = {"reactants": [], "products": [], "k": 1.0}  # Default k value is 1.0

    if request.method == "POST":
        # Reset reaction before adding new data
        python_reaction.reset()
        
        # Get form data
        reactants = request.form.getlist("reactant_name")
        reactant_degrees = request.form.getlist("reactant_degree")
        reactant_concentrations = request.form.getlist("reactant_concentration")
        reactant_eq_concentrations = request.form.getlist("reactant_eq_conc")  # New field

        products = request.form.getlist("product_name")
        product_degrees = request.form.getlist("product_degree")
        product_concentrations = request.form.getlist("product_concentration")
        product_eq_concentrations = request.form.getlist("product_eq_conc")  # New field

        # Reaction constant k
        k = request.form.get("k", 1.0)  # Default value of 1.0 if not provided

        # Fill in the reaction data for reactants and products
        reaction_data["reactants"] = [
            {"name": r, "degree": d, "concentration": c, "eq_conc": eq_c}
            for r, d, c, eq_c in zip(reactants, reactant_degrees, reactant_concentrations, reactant_eq_concentrations) if r.strip()
        ]
        reaction_data["products"] = [
            {"name": p, "degree": d, "concentration": c, "eq_conc": eq_c}
            for p, d, c, eq_c in zip(products, product_degrees, product_concentrations, product_eq_concentrations) if p.strip()
        ]
        
        # Add reactants and products to the Python reaction model
        for reactant in reaction_data["reactants"]:
            python_reaction.add_molecule(
                name=reactant["name"], 
                degree=int(reactant["degree"]), 
                initial_concentration=float(reactant["concentration"]),
                eq_conc=float(reactant["eq_conc"]), 
                is_product=False
            )
        
        for product in reaction_data["products"]:
            python_reaction.add_molecule(
                name=product["name"], 
                degree=int(product["degree"]), 
                initial_concentration=float(product["concentration"]),
                eq_conc=float(product["eq_conc"]),  # Pass eq_conc
                is_product=True
            )
        
        # Set the reaction constant k
        python_reaction.set_k(float(k))
        
        # Generate the reaction graph
        python_reaction.make_graph(link="static/images/")
    
    # Render the template with updated reaction data
    return render_template("test.html", reaction=reaction_data)
