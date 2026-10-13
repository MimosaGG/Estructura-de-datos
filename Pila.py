import tkinter as tk
from tkinter import messagebox


class StackVisualizer:

  def __init__(self, root):
    self.root = root
    self.root.title(" Gráfico de Pila")
    self.root.geometry("450x550")
    self.root.config(bg="#f0f2f5")

    self.stack = []
    self.max_size = 8  

    
    title_label = tk.Label(
        root,
        text="Simulador de una Pila ",
        font=("Arial", 16, "bold"),
        bg="#f0f2f5",
        fg="#333",
    )
    title_label.pack(pady=10)

    
    control_frame = tk.Frame(root, bg="#f0f2f5")
    control_frame.pack(pady=10)

    self.entry = tk.Entry(control_frame, font=("Arial", 12), width=10)
    self.entry.pack(side=tk.LEFT, padx=5)
    self.entry.focus()
    
    self.entry.bind("<Return>", lambda event: self.push())

    push_btn = tk.Button(
        control_frame,
        text="Apilar (Push)",
        command=self.push,
        bg="#4CAF50",
        fg="white",
        font=("Arial", 10, "bold"),
    )
    push_btn.pack(side=tk.LEFT, padx=5)

    pop_btn = tk.Button(
        control_frame,
        text="Desapilar (Pop)",
        command=self.pop,
        bg="#f44336",
        fg="white",
        font=("Arial", 10, "bold"),
    )
    pop_btn.pack(side=tk.LEFT, padx=5)

    clear_btn = tk.Button(
        control_frame,
        text="Limpiar",
        command=self.clear,
        bg="#ff9800",
        fg="white",
        font=("Arial", 10, "bold"),
    )
    clear_btn.pack(side=tk.LEFT, padx=5)

    
    self.canvas = tk.Canvas(
        root, width=280, height=320, bg="white", highlightthickness=1
    )
    self.canvas.pack(pady=10)

    
    self.status_label = tk.Label(
        root,
        text=(
            "Pila vacía. Ingresa un valor y presiona 'Apilar' o la tecla Enter."
        ),
        font=("Arial", 9, "italic"),
        bg="#f0f2f5",
        fg="#555",
    )
    self.status_label.pack(pady=5)

    
    self.draw_stack()

  def push(self):
    val = self.entry.get().strip()
    if not val:
      messagebox.showwarning("Advertencia", "Por favor ingresa un valor.")
      return
    if len(self.stack) >= self.max_size:
      messagebox.showerror(
          "Error (Overflow)",
          f"La pila está llena (Máximo {self.max_size} elementos).",
      )
      return

    self.stack.append(val)
    self.entry.delete(0, tk.END)
    self.status_label.config(text=f"Elemento '{val}' apilado con éxito.")
    self.draw_stack()

  def pop(self):
    if not self.stack:
      messagebox.showwarning("Advertencia", "La pila está vacía (Underflow).")
      return

    val = self.stack.pop()
    self.status_label.config(text=f"Elemento '{val}' desapilado.")
    self.draw_stack()

  def clear(self):
    self.stack.clear()
    self.status_label.config(text="La pila ha sido reiniciada.")
    self.draw_stack()

  def draw_stack(self):
    self.canvas.delete("all")
    width = 280
    height = 320
    box_height = 32
    box_width = 140
    start_x = (width - box_width) // 2 - 20
    start_y = height - 20  

    
    self.canvas.create_line(
        start_x - 5,
        height - 10,
        start_x - 5,
        height - (self.max_size * box_height) - 15,
        width=3,
        fill="#333",
    )
    self.canvas.create_line(
        start_x + box_width + 5,
        height - 10,
        start_x + box_width + 5,
        height - (self.max_size * box_height) - 15,
        width=3,
        fill="#333",
    )
    self.canvas.create_line(
        start_x - 5,
        height - 10,
        start_x + box_width + 5,
        height - 10,
        width=3,
        fill="#333",
    )

    
    for i, val in enumerate(self.stack):
      y1 = start_y - (i * box_height)
      y0 = y1 - box_height

      
      is_top = i == len(self.stack) - 1
      fill_color = "#4CAF50" if is_top else "#e0e0e0"
      text_color = "white" if is_top else "black"

      
      self.canvas.create_rectangle(
          start_x,
          y0,
          start_x + box_width,
          y1,
          fill=fill_color,
          outline="#333",
          width=2,
      )
      
      self.canvas.create_text(
          start_x + box_width // 2,
          (y0 + y1) // 2,
          text=str(val),
          font=("Arial", 11, "bold"),
          fill=text_color,
      )

      
      if is_top:
        self.canvas.create_text(
            start_x + box_width + 45,
            (y0 + y1) // 2,
            text="<-- CIMA",
            font=("Arial", 9, "bold"),
            fill="#d32f2f",
        )


if __name__ == "__main__":
  root = tk.Tk()
  app = StackVisualizer(root)
  root.mainloop()
