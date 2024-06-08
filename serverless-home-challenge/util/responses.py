import json

class Responses:
    @staticmethod
    def _200(data):
        if data is None:
            data = {}
        return {
            'statusCode': 200,
            'body': data
        }
    @staticmethod
    def _201(data):
        if data is None:
            data = {}
        return {
            'statusCode': 201,
            'body': data
        }

    @staticmethod
    def _204(data):
        if data is None:
            data = {}
        return {
            'statusCode': 204,
            'body': data
        }

    @staticmethod
    def _400(data):
        if data is None:
            data = {}
        return {
            'statusCode': 400,
            'body': data
        }
    
    @staticmethod
    def _404(data):
        if data is None:
            data = {}
        return {
            'statusCode': 404,
            'body': data
        }
    
    @staticmethod
    def _409(data):
        if data is None:
            data = {}
        return {
            'statusCode': 409,
            'body': data
        }

    @staticmethod
    def _500(data):
        if data is None:
            data = {}
        return {
            'statusCode': 500,
            'body': data
        }