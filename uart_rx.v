module uart_rx #(parameter CLKS_PER_BIT = 10416) (
    input        i_Clock,       
    input        i_Rx_Serial,   
    output       o_Rx_DV,       
    output [7:0] o_Rx_Byte      
);
    // State machine states
    localparam IDLE         = 3'b000;
    localparam RX_START_BIT = 3'b001;
    localparam RX_DATA_BITS = 3'b010;
    localparam RX_STOP_BIT  = 3'b011;
    localparam CLEANUP      = 3'b100;

    // Synchronizer registers (to prevent metastability)
    reg r_Rx_Data_R = 1'b1;
    reg r_Rx_Data   = 1'b1;

    reg [13:0] r_Clk_Count = 0;
    reg [2:0]  r_Bit_Index = 0;
    reg [7:0]  r_Rx_Byte   = 0;
    reg        r_Rx_DV     = 0;
    reg [2:0]  r_SM_Main   = 0;

    // Double-register the incoming data
    always @(posedge i_Clock) begin
        r_Rx_Data_R <= i_Rx_Serial;
        r_Rx_Data   <= r_Rx_Data_R;
    end

    always @(posedge i_Clock) begin
        case (r_SM_Main)
            IDLE : begin
                r_Rx_DV     <= 1'b0;
                r_Clk_Count <= 0;
                r_Bit_Index <= 0;
                // Use the synchronized r_Rx_Data instead of i_Rx_Serial
                if (r_Rx_Data == 1'b0) r_SM_Main <= RX_START_BIT; 
                else r_SM_Main <= IDLE;
            end

            RX_START_BIT : begin
                if (r_Clk_Count == (CLKS_PER_BIT-1)/2) begin
                    if (r_Rx_Data == 1'b0) begin
                        r_Clk_Count <= 0;
                        r_SM_Main   <= RX_DATA_BITS;
                    end else r_SM_Main <= IDLE;
                end else begin
                    r_Clk_Count <= r_Clk_Count + 1;
                    r_SM_Main   <= RX_START_BIT;
                end
            end

            RX_DATA_BITS : begin
                if (r_Clk_Count < CLKS_PER_BIT-1) begin
                    r_Clk_Count <= r_Clk_Count + 1;
                    r_SM_Main   <= RX_DATA_BITS;
                end else begin
                    r_Clk_Count            <= 0;
                    r_Rx_Byte[r_Bit_Index] <= r_Rx_Data;
                    if (r_Bit_Index < 7) begin
                        r_Bit_Index <= r_Bit_Index + 1;
                        r_SM_Main   <= RX_DATA_BITS;
                    end else begin
                        r_Bit_Index <= 0;
                        r_SM_Main   <= RX_STOP_BIT;
                    end
                end
            end

            RX_STOP_BIT : begin
                if (r_Clk_Count < CLKS_PER_BIT-1) begin
                    r_Clk_Count <= r_Clk_Count + 1;
                    r_SM_Main   <= RX_STOP_BIT;
                end else begin
                    r_Rx_DV     <= 1'b1; 
                    r_Clk_Count <= 0;
                    r_SM_Main   <= CLEANUP;
                end
            end

            CLEANUP : begin
                r_SM_Main <= IDLE;
                r_Rx_DV   <= 1'b0;
            end

            default : r_SM_Main <= IDLE;
        endcase
    end

    assign o_Rx_DV   = r_Rx_DV;
    assign o_Rx_Byte = r_Rx_Byte;
endmodule
