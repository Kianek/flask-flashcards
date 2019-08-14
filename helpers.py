from flask_restful import reqparse


def init_parser():
    return reqparse.RequestParser()


# def create_parser()


def hash_password(password):
    from app import flask_bcrypt

    return flask_bcrypt.generate_password_hash(password)
