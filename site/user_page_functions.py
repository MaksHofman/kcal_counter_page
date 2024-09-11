from models import db, User

def update_goal_by_email(email, goal):
    user = User.query.filter_by(email=email).first()

    if user:
        user.goal = goal
        db.session.commit()
    else:
        raise ValueError("User does not exist")