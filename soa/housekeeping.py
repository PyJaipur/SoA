from soa import models


def handle(args):
    def add_perm():
        email, *perm = input("email *perm:").split()
        session = models.Session()
        u = session.query(models.User).filter_by(email=email).first()
        if u is not None:
            u.permissions = list(set(u.permissions + perm))
            session.commit()
        session.close()

    def clear_db():
        models.engine.execute(
            """
        delete from logintoken ;
        drop table logintoken ;
        delete from "user" ;
        drop table "user" ;
        """
        )

    # Call the specified function
    exec(f"{args.housekeeping}()", globals(), locals())
