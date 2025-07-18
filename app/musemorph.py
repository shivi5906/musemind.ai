from app.versecraftAgent import VerseCraftAgent
from app.plotweaaver import PlotWeaver

# musemorph_agent.py

# Import your two existing agents



class MuseMorphAgent:
    def __init__(self):
        self.versecraft = VerseCraftAgent()
        self.plotweaver = PlotWeaver()

    def morph(self, raw_thought: str, desired_output: str) -> str:
        desired_output = desired_output.lower().strip()

        if desired_output == "freeverse":
            # Send raw_thought to VerseCraft (with default mood/keywords if needed)
            return self.versecraft.generate_poem_from_raw(raw_thought)

        elif desired_output == "structuredpoem":
            # Send raw_thought to PlotWeaver (genre + structure)
            return self.versecraft.generate_poem_from_raw2(raw_thought)

        elif desired_output == "philosophicalreflection":
            # Simple structured reflection (can be enhanced later)
            return self.plotweaver.generate_philosophical_reflection(raw_thought)
        else:
            return "❌ Unsupported output format selected."

    def reflect_on_thought(self, text: str) -> str:
        # Simple philosophical reflection — can later be replaced with a chain
        return f"[Reflection Mode]\n'{text}'\nmakes us question reality itself."


# ✅ Example Usage
if __name__ == "__main__":
    musemorph = MuseMorphAgent()

    raw_thought = "The sky turned pink as the city fell silent."
    desired_output = "structuredpoem"  # Try: freeverse, structuredpoem, philosophicalreflection

    result = musemorph.morph(raw_thought, desired_output)

    print("\n🧠 MuseMorph Output:\n")
    print(result["poem"])
    raw_thought = "The sky turned pink as the city fell silent."
    desired_output = "philosophicalreflection"  # Try: freeverse, structuredpoem, philosophicalreflection

    result = musemorph.morph(raw_thought, desired_output)

    print("\n🧠 MuseMorph Output:\n")
    print(result['reflection'])

    raw_thought = "The sky turned pink as the city fell silent."
    desired_output = "freeverse"  # Try: freeverse, structuredpoem, philosophicalreflection

    result = musemorph.morph(raw_thought, desired_output)

    print("\n🧠 MuseMorph Output:\n")
    print(result["poem"])