export default function formatDate(time: string) {
    const date = new Date(time);
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString();
}