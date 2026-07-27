import { useState } from "react";

import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { tomorrow } from "react-syntax-highlighter/dist/esm/styles/prism";

function ChatMessage({ role, content, sources }) {

  const [copied, setCopied] = useState(false);

  const isUser = role === "user";
  const isLoading = content === "__LOADING__";

  const copyResponse = async () => {

    try {

      await navigator.clipboard.writeText(content);

      setCopied(true);

      setTimeout(() => {
        setCopied(false);
      }, 2000);

    } catch (error) {

      console.error(error);

    }

  };

  // Remove duplicate filename + page combinations
  const uniqueSources =
    sources
      ? [
          ...new Map(
            sources.map((source) => [
              `${source.filename}-${source.page}`,
              source,
            ])
          ).values(),
        ]
      : [];

  return (

    <div
      className={`mb-4 flex ${
        isUser ? "justify-end" : "justify-start"
      }`}
    >

      <div
        className={`max-w-4xl rounded-lg px-4 py-3 ${
          isUser
            ? "bg-blue-600 text-white"
            : "bg-white border shadow-sm"
        }`}
      >

        {/* Copy Button */}

        {!isUser && !isLoading && (

          <div className="flex justify-end mb-2">

            <button
              onClick={copyResponse}
              className="text-sm text-blue-600 hover:text-blue-800"
            >
              {copied ? "✅ Copied" : "📋 Copy"}
            </button>

          </div>

        )}

        {/* Loading */}

        {isLoading ? (

          <div className="flex items-center gap-3">

            <div className="animate-pulse text-2xl">
              🤖
            </div>

            <div className="text-gray-500 font-medium">
              AI is thinking...
            </div>

          </div>

        ) : isUser ? (

          <p className="whitespace-pre-wrap">
            {content}
          </p>

        ) : (

          <ReactMarkdown
            remarkPlugins={[remarkGfm]}
            components={{

              code({
                inline,
                className,
                children,
                ...props
              }) {

                const match =
                  /language-(\w+)/.exec(
                    className || ""
                  );

                return !inline && match ? (

                  <SyntaxHighlighter
                    style={tomorrow}
                    language={match[1]}
                    PreTag="div"
                  >
                    {String(children).replace(/\n$/, "")}
                  </SyntaxHighlighter>

                ) : (

                  <code
                    className="bg-gray-200 rounded px-1"
                    {...props}
                  >
                    {children}
                  </code>

                );

              },

            }}
          >
            {content}
          </ReactMarkdown>

        )}

        {/* Sources */}

        {!isUser &&
          !isLoading &&
          uniqueSources.length > 0 && (

          <div className="mt-5 border-t pt-3">

            <h4 className="font-semibold text-sm mb-3">
              📄 Sources
            </h4>

            {uniqueSources.map((source, index) => (

              <div
                key={index}
                className="mb-2 rounded-lg border bg-gray-50 p-3"
              >

                <div className="font-medium">
                  📄 {source.filename}
                </div>

                <div className="text-gray-600 text-sm mt-1">
                  Page {source.page}
                </div>

              </div>

            ))}

          </div>

        )}

      </div>

    </div>

  );

}

export default ChatMessage;