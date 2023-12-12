class entity_list: 
    def __init__(self, entities=[]):
        self.entities = entities

    def add(self, entity): 
        self.entities += entity 

    def add(self, entities): 
        self.entities.extend(entities) 

    def update_locations(self): 
        for entity in self.entities: 
            entity.update_location() 

    def draw(self, screen): 
        for entity in self.entities: 
            entity.draw(screen) 