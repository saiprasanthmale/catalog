from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import datetime
from setup_file import *

engine = create_engine('sqlite:///college_db.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

# Existing College_Name delete
session.query(College_Name).delete()
# Existing Student_Details delete
session.query(Student_Details).delete()
# Existing Student_Details delete.
session.query(User).delete()

# user data
User1 = User(name="SaiPrasanth", email="saiprasanthmale@gmail.com",)
session.add(User1)
session.commit()
print ("User added successfully")
# sample data
College1 = College_Name(name="NEC", user_id=1)
session.add(College1)
session.commit()

College2 = College_Name(name="VIT", user_id=1)
session.add(College2)
session.commit()

College3 = College_Name(name="RVR", user_id=1)
session.add(College3)
session.commit()

College4 = College_Name(name="VR", user_id=1)
session.add(College4)
session.commit()

College5 = College_Name(name="SRM", user_id=1)
session.add(College5)
session.commit()
# Using different users for details
Student1 = Student_Details(stu_name="Prasanth.M", stu_rnumber="17471A0564",
                           stu_phone_number="6300548978",
                           stu_course="B.Tech",
                           stu_address=("Guntur"),
                           slink=("https://data.whicdn.com"
                                  "/images/217038319/large.jpg"),
                           college_name_id=1,
                           user_id=1)
session.add(Student1)
session.commit()

Student2 = Student_Details(stu_name="Mahe", stu_rnumber="17471A05A6",
                           stu_phone_number="84569748978",
                           stu_course="B.Tech",
                           stu_address=("Vijayawada"),
                           slink=("https://i.pinimg.com/736x/79"
                                  "/d4/b7/79d4b7199f5dcc593bc289011f61912b"
                                  "--teenage-boy-hairstyles-boys"
                                  "-haircuts-.jpg?b=t"),
                           college_name_id=2,
                           user_id=1)
session.add(Student2)
session.commit()

Student3 = Student_Details(stu_name="Maddi", stu_rnumber="16471A0456",
                           stu_phone_number="7569841236",
                           stu_course="B.Tech",
                           stu_address=("Nandigama"),
                           slink=("https://boys-brigade.org.uk"
                                  "/wp-content/themes/Boysbrigade"
                                  "/images/senior.jpg"),
                           college_name_id=3,
                           user_id=1)
session.add(Student3)
session.commit()

Student4 = Student_Details(stu_name="Kristen", stu_rnumber="1656",
                           stu_phone_number="9755454236",
                           stu_course="B.Tech",
                           stu_address=("Tripura"),
                           slink=("https://img.kpopmap.com"
                                  "/2016/05/yeonsuk.jpg"),
                           college_name_id=4,
                           user_id=1)
session.add(Student4)
session.commit()

Student5 = Student_Details(stu_name="Luis", stu_rnumber="146",
                           stu_phone_number="6987451203",
                           stu_course="B.Tech",
                           stu_address=("Atlant"),
                           slink=("https://img.kpopmap.com"
                                  "/2017/11/Kim-DongYoon.jpg"),
                           college_name_id=5,
                           user_id=1)
session.add(Student5)
session.commit()
print("Collegedata has been inserted sucessfully in the database")
