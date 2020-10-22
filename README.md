# Suggested Time
> suggested_time is a function that returns the possible meeting time for 2 people

## Getting Started

### Prerequisites
- Docker
- Docker Compose

### Running the tests
```
$ docker-compose up --build
```

## Parameters
list_1 : list of str

    List of 1st users current meeting schedule

list_2: list of str

    List of 2nd users current meeting schedule
    
start_time: str

    Time after which possible meeting time should be suggested
    
end_time: str

    Time before which possible meeting should be scheduled

duration: int

    Duration of the meeting in minutes


## Improvements
- Handle more edge cases like end_time > start_time, incorrect time values, etc. These were not handled in order to 
keep code clean and simple


## Reference 
- https://stackoverflow.com/questions/34425237/algorithm-to-find-meeting-time-slots-where-all-participants-are-available