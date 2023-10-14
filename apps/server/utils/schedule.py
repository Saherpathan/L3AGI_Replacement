from models.schedule import ScheduleModel
from utils.user import convert_model_to_response as user_convert_model_to_response
from typing import List, Optional
from typings.schedule import ScheduleOutput, ConfigsOutput, ScheduleInput, ScheduleWithConfigsOutput
from utils.type import convert_value_to_type


def convert_model_to_response(schedule_model: ScheduleModel) -> ScheduleWithConfigsOutput:
    schedule_data = {}
    
    # Extract attributes from ScheduleModel using annotations of Schedule
    for key in ScheduleOutput.__annotations__.keys():
        if hasattr(schedule_model, key):
            target_type = ScheduleOutput.__annotations__.get(key)
            schedule_data[key] = convert_value_to_type(value=getattr(schedule_model, key), target_type=target_type)
    
    # Convert ScheduleConfigModel instances to Config
    configs = {}
    if hasattr(schedule_model, 'configs'):
        for config_model in schedule_model.configs:
            key = getattr(config_model, "key")
            value = getattr(config_model, "value")
            
            # Convert value to the type specified in ConfigsOutput
            target_type = ConfigsOutput.__annotations__.get(key)

            if target_type:
                value = convert_value_to_type(value, target_type)
            
            configs[key] = value
    
    if hasattr(schedule_model, 'creator') and schedule_model.creator:
       schedule_data['creator'] = user_convert_model_to_response(schedule_model.creator)

    
    return ScheduleWithConfigsOutput(schedule=ScheduleOutput(**schedule_data), 
                                    configs= ConfigsOutput(**configs) if configs else None )


def convert_schedules_to_schedule_list(schedules: List[ScheduleModel]) -> List[ScheduleWithConfigsOutput]:
    return [convert_model_to_response(schedule_model) for schedule_model in schedules]