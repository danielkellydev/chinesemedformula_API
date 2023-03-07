from doctor_routes import doctor_routes
from patient_routes import patient_routes
from formula_routes import formula_routes
from prescription_routes import prescription_routes

registerable_controllers = [
    doctor_routes,
    patient_routes,
    formula_routes,
    prescription_routes
]