import json
from typing import List

from marshmallow import Schema, fields, post_load, validate

MAXIMUM_NUMBER_OF_CHARACTERS_SPECIES_NAME = 64

class Species:
    def __init__(self, name: str, calories_provided: int, calories_needed: int, food_sources: List[str]):
        assert len(name) <= MAXIMUM_NUMBER_OF_CHARACTERS_SPECIES_NAME, \
            f'name should be {MAXIMUM_NUMBER_OF_CHARACTERS_SPECIES_NAME} characters or less'
        self.name = name
        assert calories_provided >= 0, 'calories provided must be a positive integer'
        self.calories_provided = calories_provided
        assert calories_needed >= 0, 'calories needed must be a positive integer'
        self.calories_needed = calories_needed
        self.food_sources = food_sources

    @classmethod
    def from_json(cls, data, many=False):
        schema = SpeciesSchema(many=many)
        if isinstance(data, dict):
            return schema.load(data)
        elif isinstance(data, str):
            json_data = json.loads(data)
            return schema.load(json_data)
        else:
            raise NotImplementedError(f"Invalid input type \'{type(data)}\' during deserialization")

    def to_json(self, format_type: str = "dict"):
        schema = SpeciesSchema()
        my_json = schema.dump(self)
        if format_type == "dict":
            return my_json
        elif format_type == "str":
            return json.dumps(my_json)
        else:
            raise NotImplementedError(f"Invalid format type \'{format_type}\' during serialization")


class SpeciesSchema(Schema):
    """
        A marshmallow schema for the Species class.
    """
    name = fields.Str(required=True, validate=validate.Length(max=MAXIMUM_NUMBER_OF_CHARACTERS_SPECIES_NAME),
                      allow_none=False)
    calories_provided = fields.Int(required=True, validate=validate.Range(min=1), allow_none=False)
    calories_needed = fields.Int(validate=validate.Range(min=0), allow_none=False)
    food_sources = fields.List(fields.Str(validate=validate.Length(max=MAXIMUM_NUMBER_OF_CHARACTERS_SPECIES_NAME)), required=True)

    @post_load
    def make_species(self, data, **kwargs) -> Species:
        return Species(**data)


class OptimizationResult:
    """
        Class representing the result of the sustainable chain of species.

        Attributes:
            number_of_species (int): The total number of species in the sustainable food chain.
            species (List[str]): The list of species names ordered by their calories provided.
    """
    def __init__(self, number_of_species: int, species: List[str]):
        self.number_of_species = number_of_species
        self.species = species

    @classmethod
    def from_json(cls, data, many=False):
        schema = OptimizationResultSchema(many=many)
        if isinstance(data, dict):
            return schema.load(data)
        elif isinstance(data, str):
            json_data = json.loads(data)
            return schema.load(json_data)
        else:
            raise NotImplementedError(f"Invalid input type \'{type(data)}\' during deserialization")

    def to_json(self, format_type: str = "dict"):
        schema = OptimizationResultSchema()
        my_json = schema.dump(self)
        if format_type == "dict":
            return my_json
        elif format_type == "str":
            return json.dumps(my_json)
        else:
            raise NotImplementedError(f"Invalid format type \'{format_type}\' during serialization")


class OptimizationResultSchema(Schema):
    """
        Marshmallow schema for deserializing and serializing OptimizationResult objects.
    """
    number_of_species = fields.Integer(required=True)
    species = fields.List(fields.String(), required=True)

    @post_load
    def make_optimization_result(self, data, **kwargs) -> OptimizationResult:
        return OptimizationResult(**data)
