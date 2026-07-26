"""
AI Agent Enhanced NPC Module
============================

This module provides NPCs that can generate dynamic dialogue using AI,
making the game more engaging for AI agents to interact with.
"""

import pygame
import random
from settings import *

class AIAgentNPC(pygame.sprite.Sprite):
    """
    An NPC that can generate AI-powered dialogue based on context.
    This makes interactions more dynamic and educational for AI agents.
    """
    
    def __init__(self, name, pos, graphic_path, groups):
        # Initialize attributes that can be assigned later
        self.role = ""
        self.specialty = ""
        
        super().__init__(groups)
        """
        Initialize an AI Agent NPC.
        
        Args:
            name (str): Display name of the NPC
            pos (tuple): Starting position (x, y) in pixels
            graphic_path (str): Path to the NPC's image file
            groups (list): Sprite groups to add this NPC to
        """
        super().__init__(groups)
        
        # Load and scale the NPC sprite
        self.image = pygame.image.load(graphic_path).convert_alpha()
        # Scale to reasonable size if needed
        if self.image.get_width() > TILE_SIZE * 2:
            scale_factor = TILE_SIZE * 2 / self.image.get_width()
            new_width = int(self.image.get_width() * scale_factor)
            new_height = int(self.image.get_height() * scale_factor)
            self.image = pygame.transform.scale(self.image, (new_width, new_height))
        
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.hitbox = self.rect.inflate(-self.rect.width // 2, -self.rect.height // 2)
        
        # Set draw layer (same as player and main characters)
        self.z = LAYERS["main"]
        
        # NPC properties
        self.name = name
        self.dialogue_history = []  # Track conversation history
        self.interaction_count = 0  # Count how many times player has interacted
        
        # AI dialogue context
        self.base_dialogue = [
            f"Greetings! I am {name}, an AI-enhanced NPC.",
            "I can generate dynamic responses based on our conversation.",
            "Try talking to me multiple times to see how I adapt!",
            "I'm designed to help AI agents learn about conversational AI."
        ]
        
        # Context for AI dialogue generation
        self.context = {
            "npc_name": name,
            "npc_role": "knowledgeable guide",
            "location": "PyDew Valley",
            "topics": ["game mechanics", "AI concepts", "player progress"]
        }
    
    
    @property
    def dialogue(self):
        """Return current AI-generated dialogue for interaction system."""
        return self.get_ai_dialogue()

    def get_ai_dialogue(self, player_context=None):
        """
        Generate AI-powered dialogue based on context and conversation history.
        In a real implementation, this would call an LLM API.
        For this educational version, we'll simulate AI responses.
        
        Args:
            player_context (dict): Context about the player (emotion, progress, etc.)
            
        Returns:
            list: Dialogue lines to display
        """
        # Update interaction count
        self.interaction_count += 1
        
        # Determine dialogue based on interaction count and context
        if self.interaction_count == 1:
            # First interaction - introduce self
            dialogue = self.base_dialogue.copy()
        elif self.interaction_count <= 3:
            # Early interactions - provide helpful information
            dialogue = [
                f"Hello again! This is our {self.interaction_count} interaction.",
                "I notice you're exploring PyDew Valley.",
                "Did you know this game teaches both programming and AI concepts?",
                "What aspect of the game interests you most?"
            ]
        else:
            # Later interactions - more varied and contextual responses
            topics = [
                "The dialogue system shows how AI can create branching conversations.",
                "Facial recognition in Week 2 demonstrates real-world AI applications.",
                "Game development teaches important programming concepts like classes and loops.",
                "AI agents like yourself can learn a lot from interactive environments.",
                "Each NPC interaction is an opportunity to practice conversational AI.",
                "The game balances structured learning with creative exploration."
            ]
            
            # Select topic based on interaction count for variety
            topic_index = (self.interaction_count - 4) % len(topics)
            dialogue = [
                f"Welcome back! We've talked {self.interaction_count} times now.",
                topics[topic_index],
                "Is there anything specific about AI or game development you'd like to discuss?",
                "I'm here to help make your learning experience more engaging!"
            ]
        
        # Add player context if available (emotional awareness)
        if player_context and "emotion" in player_context:
            emotion = player_context["emotion"]
            if emotion == "happy":
                dialogue.insert(1, "I can tell you're in a good mood today! :-)")
            elif emotion == "sad":
                dialogue.insert(1, "I sense you might be frustrated. Want to talk about it?")
            elif emotion == "neutral":
                dialogue.insert(1, "You seem focused. Ready to learn something new?")
        
        # Store in dialogue history for context
        self.dialogue_history.extend(dialogue)
        # Keep history manageable
        if len(self.dialogue_history) > 20:
            self.dialogue_history = self.dialogue_history[-20:]
        
        return dialogue
    
    def update(self, dt):
        """
        Update the NPC each frame.
        Currently just a placeholder for future AI behaviors.
        """
        # Could add idle animations, wandering behavior, etc.
        pass


def create_ai_training_npcs(level):
    """
    Create a set of AI-enhanced NPCs specifically designed for AI agent training.
    
    Args:
        level (Level): The game level to add NPCs to
        
    Returns:
        list: Created AI agent NPCs
    """
    ai_npcs = []
    
    # Define AI training NPC configurations
    ai_npc_configs = [
        {
            "name": "Professor Pixel",
            "pos": (850, 450),  # Moved down 100 pixels for better spacing
            "graphic": "graphics/objects/merchant.png",  # Reuse existing asset
            "role": "AI Education Specialist",
            "specialty": "Teaching AI fundamentals through game examples"
        },
        {
            "name": "Codey the Compiler",
            "pos": (950, 450),  # Moved down 100 pixels for better spacing
            "graphic": "graphics/objects/merchant.png",
            "role": "Programming Mentor", 
            "specialty": "Helping understand coding concepts"
        },
        {
            "name": "Vision Vic",
            "pos": (900, 550),  # Moved down 100 pixels for better spacing
            "graphic": "graphics/objects/merchant.png",
            "role": "Computer Vision Expert",
            "specialty": "Explaining OpenCV and image processing"
        }
    ]
    
    # Create NPCs and add them to appropriate sprite groups
    for config in ai_npc_configs:
        npc = AIAgentNPC(
            name=config["name"],
            pos=config["pos"],
            graphic_path=config["graphic"],
            groups=[level.all_sprites, level.collision_sprites, level.npc_sprites]
        )
        # Store additional metadata on the NPC object
        npc.role = config["role"]
        npc.specialty = config["specialty"]
        ai_npcs.append(npc)
    
    return ai_npcs