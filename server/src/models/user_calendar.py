from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKeyConstraint

from models.base import Base, db


# Get all users for now, ask if Proost users have objections to this type of access 
class CalendarUser(Base):
    __tablename__ = 'calendar_user'
    __bind_key__ = 'user_db'

    # The internal Google ID
    id = db.Column(db.String(100), primary_key=True)

    primary_alias = db.Column(db.String(200))
    given_name = db.Column(db.String(200))
    family_name = db.Column(db.String(200))
    full_name = db.Column(db.String(200))
    # Should get updated with every sync
    current_calendar_timezone = db.Column(db.String(200))
    user_aliasses = relationship("CalendarUserAlias", back_populates="calendar_user")


class CalendarUserAlias(Base):
    __tablename__ = 'calendar_user_alias'
    __bind_key__ = 'user_db'
    alias = db.Column(db.String(200), primary_key=True)
    calendar_user_id = db.Column(db.String(100), db.ForeignKey('calendar_user.id'))
    calendar_user = relationship("CalendarUser", back_populates="user_aliasses")


# This table has two primary keys as the event ID is the same on all calendars, but different calendars get different details
class CalendarEvents(Base):
    __tablename__ = 'calendar_event'
    __bind_key__ = 'user_db'

    # Should be the ID from Google
    event_id = db.Column(db.String(500), primary_key=True)

    created_at = db.Column(db.TIMESTAMP)
    updated_at = db.Column(db.TIMESTAMP)

    organizer_email = db.Column(db.String(200))
    creator_email = db.Column(db.String(200))

    # The status of the event. Can be cancelled.
    status = db.Column(db.String(200))

    # Add recurrance ID
    is_recurring = db.Column(db.BOOLEAN)
    recurrence_id = db.Column(db.String(200))

    title = db.Column(db.String(500))
    location = db.Column(db.String(500))
    start_time = db.Column(db.TIMESTAMP)
    end_time = db.Column(db.TIMESTAMP)
    description = db.Column(db.Text(collation='utf8mb4_unicode_ci'))
    calendar_event_attendees = relationship("CalendarEventAttendees", back_populates="calendar_event")


# TODO need to find a way to see what timezone a user was in, and what the working hours were when an event happened. Daily snapshot of cal timezone? 
class CalendarEventAttendees(Base):
    __tablename__ = 'calendar_event_attendee'
    __bind_key__ = 'user_db'

    event_id = db.Column(db.String(500), db.ForeignKey('calendar_event.event_id'), primary_key=True)
    invited_email = db.Column(db.String(200),  primary_key=True)

    # The ID of the user that was invited, regardless of which email alias was used for the invite
    calendar_user_id = db.Column(db.String(100), db.ForeignKey('calendar_user.id'))

    # Get timezone from event if possibe. 
    timezone = db.Column(db.String(200))
    # TODO As long as this isn't available, lets assume 9-5
    working_hours_start_time = db.Column(db.TIME)
    working_hours_end_time = db.Column(db.TIME)

    # The timezone for the attendee when the event was organized
    timezone_organized = db.Column(db.String(200))

    display_name = db.Column(db.String(200))
    response_status = db.Column(db.String(20))
    is_organizer = db.Column(db.BOOLEAN)
    is_optional = db.Column(db.BOOLEAN)
    comment = db.Column(db.String(5000))

    # Don't backpopulate the calendaruser as it doesn't seem useful and there will be too many entitities
    calendar_user = relationship("CalendarUser")
    calendar_event = relationship("CalendarEvents", back_populates="calendar_event_attendees")

