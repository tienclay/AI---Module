from typing import List, Optional
from pydantic import BaseModel, EmailStr
import json
class WorkExperience(BaseModel):
    companyName: str
    position: str
    fromMonth: int
    fromYear: int
    toMonth: Optional[int]
    toYear: Optional[int]
    description: str

class Education(BaseModel):
    institutionName: str
    degree: str
    fromMonth: Optional[int]
    fromYear: int
    toMonth: Optional[int]
    toYear: int

class Language(BaseModel):
    label: str
    level: str  # Could be improved with an Enum for level validation

class Profile(BaseModel):
    firstName: str
    lastName: str
    gender: str
    dateOfBirth: str
    email: EmailStr
    phoneCode: str
    phone: str
    title: str
    summary: str
    totalExperience: str
    location: str
    workExperience: List[WorkExperience]
    education: List[Education]
    skills: List[str]
    languages: List[Language]
    
    
def get_json(model):
    json_output_prompt = "\nProvide your output as a JSON containing the following fields:"
    json_schema = model.model_json_schema()
    if json_schema is not None:
        output_model_properties = {}
        json_schema_properties = json_schema.get("properties")
        if json_schema_properties is not None:
            for field_name, field_properties in json_schema_properties.items():
                formatted_field_properties = {
                    prop_name: prop_value
                    for prop_name, prop_value in field_properties.items()
                    if prop_name != "title"
                }
                output_model_properties[field_name] = formatted_field_properties
        json_schema_defs = json_schema.get("$defs")
        if json_schema_defs is not None:
            output_model_properties["$defs"] = {}
            for def_name, def_properties in json_schema_defs.items():
                def_fields = def_properties.get("properties")
                formatted_def_properties = {}
                if def_fields is not None:
                    for field_name, field_properties in def_fields.items():
                        formatted_field_properties = {
                            prop_name: prop_value
                            for prop_name, prop_value in field_properties.items()
                            if prop_name != "title"
                        }
                        formatted_def_properties[field_name] = formatted_field_properties
                if len(formatted_def_properties) > 0:
                    output_model_properties["$defs"][def_name] = formatted_def_properties

        if len(output_model_properties) > 0:
            json_output_prompt += "\n<json_fields>"
            json_output_prompt += f"\n{json.dumps(list(output_model_properties.keys()))}"
            json_output_prompt += "\n</json_fields>"
            json_output_prompt += "\nHere are the properties for each field:"
            json_output_prompt += "\n<json_field_properties>"
            json_output_prompt += f"\n{json.dumps(output_model_properties, indent=2)}"
            json_output_prompt += "\n</json_field_properties>"
    return json_output_prompt    
            
print(get_json(Profile))