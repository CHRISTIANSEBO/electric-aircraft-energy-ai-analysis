# Electric Aircraft Energy Analysis Tool (Physics + ML)

🚀 Physics-based electric aircraft energy analysis tool with integrated machine learning prediction and interactive trade study visualization.

Built using aerodynamic modeling principles and trained regression models to compare first-principles simulation against data-driven approximation.


## Overview

This project models the energy requirements of an electric aircraft during steady cruise flight using first-principles aerodynamics, and compares the physics-based calculation with a machine learning regression model trained on synthetic mission data.

The application includes:

- Physics-based cruise energy model  
- Synthetic mission dataset generation  
- ML regression training and evaluation  
- ML vs physics prediction comparison  
- Trade study visualization (Energy vs Speed)  
- Interactive web interface using Flask  

The goal of the project is to explore how data-driven models approximate nonlinear aerodynamic behavior and evaluate prediction error relative to a ground-truth physics model.


---

## Physics Model

Cruise performance is modeled using a simplified drag polar:

CD = CD0 + k·CL²  

Lift is calculated from steady-level flight equilibrium:

Lift = Weight  

Drag force:

D = 0.5 · ρ · V² · S · CD  

Power required:

P = (Drag · Velocity) / η  

Energy is computed over mission distance and converted to kWh.

Assumptions:

- Steady, level cruise
- Constant velocity
- No wind
- Exponential atmospheric density model
- No climb or descent segments

This produces physically meaningful behavior, including a minimum-energy cruise speed due to induced vs parasite drag trade-offs.


---

## Machine Learning Model

A synthetic dataset is generated using the physics model across randomized mission parameters:

- Mass: 500–800 kg  
- Speed: 35–85 m/s  
- Distance: 50–150 miles  
- Altitude: 0–10,000 ft  

Energy (kWh) is computed as ground truth.

A Linear Regression model is trained to predict mission energy from:

[mass, speed, distance, altitude]

The model is evaluated using Mean Squared Error (MSE) and integrated into the web app for real-time comparison against the physics result.

This demonstrates:

- Data generation from simulation  
- Model training and validation  
- Error evaluation  
- Deployment of trained model  


---

## Trade Study Visualization

For each mission input, the tool generates an Energy vs Cruise Speed curve.

This visualizes the nonlinear energy response to speed and highlights the existence of a minimum-energy cruise region.

The trade study supports:

- Design sensitivity analysis  
- Energy optimization insight  
- Systems-level performance reasoning  


---

## Project Structure

electric-aircraft-energy-calculator/
│
├── src/
│   ├── energy_calc.py
│   ├── generate_dataset.py
│   └── train_model.py
│
├── web/
│   ├── app.py
│   └── templates/
│       └── index.html
│
├── dataset.csv
├── energy_model.pkl
└── requirements.txt


---

## Installation

Install dependencies:

python -m pip install -r requirements.txt

Generate dataset:

python src/generate_dataset.py

Train ML model:

python src/train_model.py

Run web application:

python web/app.py

Then open:

http://127.0.0.1:5000/


---

## Example Output

For a 650 kg aircraft, 100-mile cruise at 60 m/s:

Physics Model:
- Energy: 38.42 kWh  

ML Prediction:
- Predicted Energy: ~41 kWh  
- Absolute Error: ~2–3 kWh  

The ML model approximates the nonlinear physics behavior but introduces prediction error due to linear assumptions.


---

## Engineering Significance

This project demonstrates:

- Aerodynamic modeling fundamentals  
- Systems-level energy analysis  
- Data-driven approximation of nonlinear physics  
- ML evaluation against simulation ground truth  
- Visualization for performance trade studies  
- Deployment of integrated AI system  

It serves as a foundational exploration of combining aerospace modeling with applied machine learning.


---

## Future Extensions

- Replace Linear Regression with Random Forest or Gradient Boosting  
- Add climb/descent mission segments  
- Incorporate solar-electric hybrid modeling  
- Perform residual analysis visualization  
- Deploy publicly to cloud platform  
