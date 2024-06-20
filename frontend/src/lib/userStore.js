import { writable } from 'svelte/store';

const createUserStore = () => {
    const storedUser = typeof sessionStorage !== 'undefined' ? JSON.parse(sessionStorage.getItem('user')) : null;
    const store = writable(storedUser);

    return {
        subscribe: store.subscribe,
        set: (user) => {
            if (typeof sessionStorage !== 'undefined') {
                sessionStorage.setItem('user', JSON.stringify(user));
            }
            store.set(user);
        },
        reset: () => {
            if (typeof sessionStorage !== 'undefined') {
                sessionStorage.removeItem('user');
            }
            store.set(null);
        }
    };
};

export const user = createUserStore();