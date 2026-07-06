import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [topics, setTopics] = useState([]);
  const [selectedTopic, setSelectedTopic] = useState(null);
  const [quizzes, setQuizzes] = useState([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState([]);
  const [currentQuiz, setCurrentQuiz] = useState(null);
  const [answer, setAnswer] = useState(null);

  useEffect(() => {
    fetch('/api/topics')
      .then(res => res.json())
      .then(data => setTopics(data))
      .catch(err => console.error('Error fetching topics:', err));
  }, []);

  const handleTopicSelect = (topic) => {
    setSelectedTopic(topic);
    fetch(`/api/quizzes/topic/${topic}`)
      .then(res => res.json())
      .then(data => setQuizzes(data))
      .catch(err => console.error('Error fetching quizzes:', err));
    setAnswer(null); // Clear previous answer when changing topic
  };

  const handleSearch = (e) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      fetch(`/api/quizzes/search/${searchQuery}`)
        .then(res => res.json())
        .then(data => setSearchResults(data))
        .catch(err => console.error('Error searching quizzes:', err));
    } else {
      setSearchResults([]);
    }
  };

  const handleQuizClick = (quiz) => {
    setCurrentQuiz(quiz);
    fetch(`/api/quiz/${quiz.id}/answer`)
      .then(res => res.json())
      .then(data => setAnswer(data))
      .catch(err => console.error('Error fetching answer:', err));
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Generative AI Quiz</h1>
      </header>
      <main>
        <section className="topics-section">
          <h2>Topics</h2>
          <ul>
            {topics.map(topic => (
              <li key={topic} onClick={() => handleTopicSelect(topic)} className={selectedTopic === topic ? 'selected' : ''}>
                {topic}
              </li>
            ))}
          </ul>
        </section>

        <section className="quizzes-section">
          <h2>{selectedTopic ? `${selectedTopic} Quizzes` : 'Quizzes'}</h2>
          {selectedTopic && (currentQuiz ? (
            <div>
              <h3>{currentQuiz.question}</h3>
              {answer && (
                <div>
                  <h4>Answer:</h4>
                  <p>{answer.explanation}</p>
                </div>
              )}
            </div>
          ) : (
            <ul>
              {quizzes.map(quiz => (
                <li key={quiz.id} onClick={() => handleQuizClick(quiz)}>
                  {quiz.question}
                </li>
              ))}
            </ul>
          ))}
        </section>

        <section className="search-section">
          <h2>Search Quizzes</h2>
          <form onSubmit={handleSearch}>
            <input 
              type="text" 
              value={searchQuery} 
              onChange={(e) => setSearchQuery(e.target.value)} 
              placeholder="Search by keyword..."
            />
            <button type="submit">Search</button>
          </form>
          {searchResults.length > 0 && (
            <div>
              <h3>Search Results:</h3>
              <ul>
                {searchResults.map(quiz => (
                  <li key={quiz.id} onClick={() => handleQuizClick(quiz)}>
                    {quiz.question} ({quiz.topic})
                  </li>
                ))}
              </ul>
            </div>
          )}
        </section>
      </main>
    </div>
  );
}

export default App;
