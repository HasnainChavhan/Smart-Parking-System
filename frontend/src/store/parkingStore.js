import { create } from 'zustand';

const useParkingStore = create((set) => ({
    lots: [],
    currentLot: null,
    slots: [],
    selectedSlot: null,

    setLots: (lots) => set({ lots }),

    setCurrentLot: (lot) => set({ currentLot: lot, slots: lot?.slots || [] }),

    setSlots: (slots) => set({ slots }),

    updateSlotStatus: (slotId, status) => set((state) => ({
        slots: state.slots.map((slot) =>
            slot.id === slotId ? { ...slot, status } : slot
        ),
    })),

    setSelectedSlot: (slot) => set({ selectedSlot: slot }),

    clearSelectedSlot: () => set({ selectedSlot: null }),
}));

export default useParkingStore;
