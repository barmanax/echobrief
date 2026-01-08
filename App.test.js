import { render, screen } from "@testing-library/react";
import App from "./App";

test("renders EchoBrief header", () => {
  render(<App />);
  expect(screen.getByText(/EchoBrief/i)).toBeInTheDocument();
});
