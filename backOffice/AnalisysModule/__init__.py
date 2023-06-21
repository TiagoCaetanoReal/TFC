from flask import Blueprint, flash, request
from flask import redirect, render_template, url_for
from forms import FuncionarioLoginForm
from models import db, Funcionario, Loja, Secção, Mapa
from flask_login import login_user, logout_user, current_user
from datetime import datetime, timedelta

MapsModule = Blueprint("MapsModule", __name__)


@MapsModule.route("/MapsList", methods=['GET', 'POST'])
def seeMapList():
    form = FuncionarioLoginForm()
    active_user = current_user

    #Select Funcionario.nome, Funcionario.cargo, Secção.nome
    # From Funcionario
    # JOIN Secção on Funcionario.Secção_id = Secção.id

    
    departemant = db.session.query(Secção).filter(Secção.id==active_user.secção_id).first()
    employee = [active_user.nome,active_user.cargo,departemant.nome]
   
#    userRides = db.session.query(Ride).filter(Ride.user_id==activeUser.id).all()
#    userReservations = db.session.query(Reservation).filter(Reservation.passenger_id==activeUser.id).all()
   
#    rideCount = len(userRides)
#    reservationCount = len(userReservations)
  
#    nextReservations = db.session.query(Vehicle, Ride, User, Reservation, ReservationState).filter(
#       Reservation.ride_id == Ride.id).filter(Reservation.passenger_id == activeUser.id).filter(
#       Reservation.reservation_state_id == ReservationState.id).filter(Ride.vehicle_id == Vehicle.id).filter(
#       User.id== Ride.user_id).order_by(Ride.ride_scheduled_time.desc()).limit(3).all()

    print(current_user)

    return render_template("ListagemMapas.html", title = "MapList", frontForm = form, active_user = employee)