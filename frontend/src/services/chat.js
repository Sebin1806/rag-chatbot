import API from "./api";

export async function askQuestion(question) {
    const response = await API.post("/chat", {
        question: question,
    });

    return response.data;
}