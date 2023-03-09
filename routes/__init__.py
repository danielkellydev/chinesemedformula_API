from routes.doctor_routes import doctor_routes
from routes.patient_routes import patient_routes
from routes.formula_routes import formula_routes
from routes.prescription_routes import prescription_routes
from routes.auth import auth_routes

registerable_controllers = [
    doctor_routes,
    patient_routes,
    formula_routes,
    prescription_routes, 
    auth_routes
]