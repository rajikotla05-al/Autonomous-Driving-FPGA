module top_steering(
    input clk,           // 100MHz clock from Basys 3
    input rx,            // UART Receive pin (Pin B18)
    output [6:0] seg,    // 7-segment cathodes {g, f, e, d, c, b, a}
    output [3:0] an      // 7-segment anodes
);

    wire [7:0] rx_byte;  
    wire rx_done;        
    // Initial state is all 1s (All segments OFF) - No dash '-'
    reg [6:0] r_seg = 7'b1111111; 

    // 1. Instantiate UART Receiver
    uart_rx #(.CLKS_PER_BIT(10416)) receiver (
        .i_Clock(clk),
        .i_Rx_Serial(rx),    
        .o_Rx_DV(rx_done),
        .o_Rx_Byte(rx_byte)
    );

    // 2. Decoder Logic (Active LOW: 0 = ON)
    always @(posedge clk) begin
        if (rx_done) begin
            case (rx_byte)
                8'h53 : r_seg <= 7'b0010010; // 'S' (Straight)
                8'h4C : r_seg <= 7'b1000111; // 'L' (Left)
                8'h52 : r_seg <= 7'b0001111; // 'r' (Right - Small r pattern)
                default: r_seg <= r_seg;     
            endcase
        end
    end

    assign seg = r_seg;
    assign an  = 4'b1110; // Only the right-most digit is active

endmodule
