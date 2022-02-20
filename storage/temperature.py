from sqlalchemy import Column, Integer, String, DateTime, Float
from base import Base


class Temperature(Base):
    """ MySQL declaretive representation of temperature Event """
    __tablename__ = "temperature"
    id = Column(Integer, primary_key=True)
    temperature_id = Column(String, nullable=False)
    temperature = Column(Float, nullable=False)
    year = Column(Integer, nullable=False)
    month = Column(Integer, nullable=False)
    day = Column(Integer, nullable=False)
    hour = Column(Integer, nullable=False)

    def __init__(self, temp_id, temp, year, month, day, hour):
        self.temperature_id = temp_id
        self.temperature = temp
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour

    def to_dict(self):
        temp = dict()
        temp['temperature_id'] = self.temperature_id
        temp['temperature'] = self.temperature
        temp['year'] = self.year
        temp['month'] = self.month
        temp['day'] = self.day
        temp['hour'] = self.hour

        return temp
