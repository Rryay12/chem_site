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
        
        # Reaction constant k
        k = request.form.getlist("k")[0]

        products = request.form.getlist("product_name")
        product_degrees = request.form.getlist("product_degree")
        product_concentrations = request.form.getlist("product_concentration")

        # Fill in the reaction data for reactants and products
        reaction_data["reactants"] = [
            {"name": r, "degree": d, "concentration": c}
            for r, d, c in zip(reactants, reactant_degrees, reactant_concentrations) if r.strip()
        ]
        reaction_data["products"] = [
            {"name": p, "degree": d, "concentration": c}
            for p, d, c in zip(products, product_degrees, product_concentrations) if p.strip()
        ]
        
        # Add reactants and products to the Python reaction model
        for reactant in reaction_data["reactants"]:
            python_reaction.add_molecule(reactant["name"], int(reactant["degree"]), float(reactant["concentration"]), False)
        
        for product in reaction_data["products"]:
            python_reaction.add_molecule(product["name"], int(product["degree"]), float(product["concentration"]), True)
        
        # Set the reaction constant k
        python_reaction.set_k(float(k))
        
        # Generate the reaction graph
        python_reaction.make_graph(link="static/images")
    
    # Render the template with updated reaction data
    return render_template("test.html", reaction=reaction_data)
