from . import PreferentialAttachmentSim

if __name__ == "__main__":
    sim = PreferentialAttachmentSim(40, 4, [1, 2, 3])
    print(sim.apply())
