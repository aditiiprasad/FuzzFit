"""
FuzzFit Fuzzy Logic Inference Engine
Implements fuzzy logic system for outfit and color recommendations
"""

import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

class OutfitFuzzySystem:
    """Fuzzy Logic System for Outfit and Color Recommendations"""
    
    def __init__(self):
        self.setup_fuzzy_variables()
        self.setup_fuzzy_rules()
        self.create_control_system()
        
    def setup_fuzzy_variables(self):
        """Define fuzzy variables and membership functions"""
        
        # INPUT: Temperature (0-50°C)
        self.temperature = ctrl.Antecedent(np.arange(0, 51, 1), 'temperature')
        self.temperature['cold'] = fuzz.trapmf(self.temperature.universe, [0, 0, 10, 18])
        self.temperature['mild'] = fuzz.trimf(self.temperature.universe, [15, 22, 28])
        self.temperature['warm'] = fuzz.trimf(self.temperature.universe, [25, 30, 35])
        self.temperature['hot'] = fuzz.trapmf(self.temperature.universe, [32, 38, 50, 50])
        
        # INPUT: Occasion (0-10 scale)
        self.occasion = ctrl.Antecedent(np.arange(0, 11, 1), 'occasion')
        self.occasion['casual'] = fuzz.trimf(self.occasion.universe, [0, 0, 5])
        self.occasion['formal'] = fuzz.trimf(self.occasion.universe, [3, 6, 9])
        self.occasion['festive'] = fuzz.trimf(self.occasion.universe, [7, 10, 10])
        
        # INPUT: Style (0-10 scale)
        self.style = ctrl.Antecedent(np.arange(0, 11, 1), 'style')
        self.style['minimal'] = fuzz.trimf(self.style.universe, [0, 0, 5])
        self.style['trendy'] = fuzz.trimf(self.style.universe, [3, 5, 8])
        self.style['bold'] = fuzz.trimf(self.style.universe, [6, 10, 10])
        
        # OUTPUT: Outfit Type (0-100 score)
        self.outfit = ctrl.Consequent(np.arange(0, 101, 1), 'outfit')
        self.outfit['light_casual'] = fuzz.trimf(self.outfit.universe, [0, 20, 40])
        self.outfit['smart_casual'] = fuzz.trimf(self.outfit.universe, [30, 50, 70])
        self.outfit['formal'] = fuzz.trimf(self.outfit.universe, [60, 80, 100])
        
        # OUTPUT: Color Intensity (0-100 score)
        self.color_intensity = ctrl.Consequent(np.arange(0, 101, 1), 'color_intensity')
        self.color_intensity['neutral'] = fuzz.trimf(self.color_intensity.universe, [0, 20, 40])
        self.color_intensity['cool'] = fuzz.trimf(self.color_intensity.universe, [30, 50, 70])
        self.color_intensity['vibrant'] = fuzz.trimf(self.color_intensity.universe, [60, 80, 100])
        
    def setup_fuzzy_rules(self):
        """Define fuzzy IF-THEN rules"""
        
        self.rules = [
            # Cold weather rules
            ctrl.Rule(self.temperature['cold'] & self.occasion['casual'],
                     (self.outfit['light_casual'], self.color_intensity['neutral'])),
            ctrl.Rule(self.temperature['cold'] & self.occasion['formal'],
                     (self.outfit['formal'], self.color_intensity['neutral'])),
            ctrl.Rule(self.temperature['cold'] & self.style['bold'],
                     (self.outfit['smart_casual'], self.color_intensity['vibrant'])),
            
            # Mild weather rules
            ctrl.Rule(self.temperature['mild'] & self.occasion['casual'] & self.style['minimal'],
                     (self.outfit['light_casual'], self.color_intensity['neutral'])),
            ctrl.Rule(self.temperature['mild'] & self.occasion['formal'],
                     (self.outfit['formal'], self.color_intensity['cool'])),
            ctrl.Rule(self.temperature['mild'] & self.style['trendy'],
                     (self.outfit['smart_casual'], self.color_intensity['cool'])),
            
            # Warm weather rules
            ctrl.Rule(self.temperature['warm'] & self.occasion['casual'],
                     (self.outfit['light_casual'], self.color_intensity['cool'])),
            ctrl.Rule(self.temperature['warm'] & self.occasion['formal'],
                     (self.outfit['smart_casual'], self.color_intensity['cool'])),
            ctrl.Rule(self.temperature['warm'] & self.occasion['festive'] & self.style['bold'],
                     (self.outfit['smart_casual'], self.color_intensity['vibrant'])),
            
            # Hot weather rules
            ctrl.Rule(self.temperature['hot'] & self.occasion['casual'],
                     (self.outfit['light_casual'], self.color_intensity['cool'])),
            ctrl.Rule(self.temperature['hot'] & self.occasion['formal'],
                     (self.outfit['smart_casual'], self.color_intensity['cool'])),
            ctrl.Rule(self.temperature['hot'] & self.style['bold'],
                     (self.outfit['smart_casual'], self.color_intensity['vibrant'])),
            
            # Style & Occasion fallback rules
            ctrl.Rule(self.style['minimal'], (self.outfit['light_casual'], self.color_intensity['neutral'])),
            ctrl.Rule(self.occasion['formal'], (self.outfit['formal'], self.color_intensity['cool'])),
            ctrl.Rule(self.occasion['festive'], (self.outfit['smart_casual'], self.color_intensity['vibrant']))
        ]
        
    def create_control_system(self):
        """Create and simulate the fuzzy control system"""
        self.outfit_ctrl = ctrl.ControlSystem(self.rules)
        self.outfit_sim = ctrl.ControlSystemSimulation(self.outfit_ctrl)
    
    def get_recommendation(self, temperature, occasion_val, style_val):
        """Get outfit and color recommendations"""
        # Set inputs
        self.outfit_sim.input['temperature'] = temperature
        self.outfit_sim.input['occasion'] = occasion_val
        self.outfit_sim.input['style'] = style_val
        
        # Compute the result
        self.outfit_sim.compute()
        
        # Safely extract outputs
        outfit_score = self.outfit_sim.output.get('outfit', 50)
        color_score = self.outfit_sim.output.get('color_intensity', 50)
        
        outfit_type = self._map_outfit_score(outfit_score)
        color_palette = self._map_color_score(color_score, temperature)
        outfit_details = self._get_outfit_details(outfit_type, temperature, occasion_val, style_val)
        
        return {
            'outfit_type': outfit_type,
            'outfit_score': outfit_score,
            'outfit_details': outfit_details,
            'color_palette': color_palette,
            'color_score': color_score,
            'temperature': temperature,
            'occasion': self._map_occasion(occasion_val),
            'style': self._map_style(style_val)
        }
    
    def _map_outfit_score(self, score):
        if score < 40:
            return "Light Casual"
        elif score < 70:
            return "Smart Casual"
        else:
            return "Formal Wear"
    
    def _map_color_score(self, score, temperature):
        if score < 40:
            return {'primary': ['#E8E8E8', '#D3D3D3', '#C0C0C0'],
                    'names': ['Light Grey', 'Beige', 'Off-White'],
                    'category': 'Neutral Tones'}
        elif score < 70:
            if temperature > 25:
                return {'primary': ['#87CEEB', '#98D8E8', '#B0E0E6'],
                        'names': ['Sky Blue', 'Powder Blue', 'Mint'],
                        'category': 'Cool Shades'}
            else:
                return {'primary': ['#8B4513', '#CD853F', '#D2691E'],
                        'names': ['Warm Brown', 'Tan', 'Copper'],
                        'category': 'Warm Shades'}
        else:
            return {'primary': ['#FF6B6B', '#4ECDC4', '#FFD93D'],
                    'names': ['Coral Red', 'Turquoise', 'Bright Yellow'],
                    'category': 'Vibrant Colors'}
    
    def _get_outfit_details(self, outfit_type, temp, occasion, style):
        outfits = {
            'Light Casual': {
                'cold': ['Hoodie & Jeans', 'Sweater & Casual Pants'],
                'mild': ['T-Shirt & Jeans', 'Casual Shirt & Chinos'],
                'warm': ['Light T-Shirt & Shorts', 'Tank Top & Linen Pants'],
                'hot': ['Breathable Tee & Shorts', 'Light Cotton Shirt']
            },
            'Smart Casual': {
                'cold': ['Blazer & Jeans', 'Cardigan & Dress Pants'],
                'mild': ['Button-Down & Chinos', 'Polo & Dress Pants'],
                'warm': ['Light Blazer & Linen Pants', 'Short-Sleeve Button-Down'],
                'hot': ['Linen Shirt & Trousers', 'Light Cotton Blazer']
            },
            'Formal Wear': {
                'cold': ['Full Suit & Tie', 'Three-Piece Suit'],
                'mild': ['Two-Piece Suit', 'Blazer & Dress Trousers'],
                'warm': ['Light Suit (No Tie)', 'Linen Suit'],
                'hot': ['Lightweight Suit', 'Formal Shirt & Dress Pants']
            }
        }
        if temp < 18: temp_cat = 'cold'
        elif temp < 28: temp_cat = 'mild'
        elif temp < 35: temp_cat = 'warm'
        else: temp_cat = 'hot'
        return outfits[outfit_type][temp_cat]
    
    def _map_occasion(self, val):
        if val < 4: return "Casual"
        elif val < 7: return "Formal"
        else: return "Festive"
    
    def _map_style(self, val):
        if val < 4: return "Minimal"
        elif val < 7: return "Trendy"
        else: return "Bold"
