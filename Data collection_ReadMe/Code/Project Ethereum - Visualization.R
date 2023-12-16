library(shiny)
library(readr)
library(lubridate)
library(dplyr)
library(ggplot2)
library(scales)
library(plotly)
library(shinydashboard)

df <- read_csv("Data_AllYears_Merged.csv")
df$date1 <- as.Date(df$date1, format="%m/%d/%y")

# Define UI
ui <- dashboardPage(
  dashboardHeader(title = "Plot Data"),
  dashboardSidebar(
    selectInput("agg_level", "Choose Aggregation Level",
                choices = list("Days" = "day", 
                               "Weeks" = "week",
                               "Months" = "month", 
                               "Years" = "year")),
    selectInput("var_select", "Select Variable",
                choices = setdiff(colnames(df), c("date1", "GhRepo", "GhRepo_2", "actor_login", "Year", "actor_id", "release_payload"))),
    dateRangeInput("date_range", "Select Date Range", 
                   start = min(df$date1), 
                   end = max(df$date1),
                   format = "mm/dd/yyyy"),
    selectInput("line_color", "Select Line Color", choices = c("Blue", "Red", "Green", "Black"), selected = "Blue"),
    selectInput("line_type", "Select Line Type", choices = c("Solid" = "solid", "Dashed" = "dashed"), selected = "Solid"),
    actionButton("plot", "Generate Plot"),
    tags$div(style = "text-align: center; margin-top: 10px;", 
             downloadButton('downloadOriginal', 'Download Original Data')),
    tags$div(style = "text-align: center; margin-top: 10px;", 
             downloadButton('downloadFiltered', 'Download Filtered Data'))
  ),
  dashboardBody(
    box(plotlyOutput("plot1"), width = 12)
  )
)

# Define server logic
server <- function(input, output) {
  
  get_filtered_data <- reactive({
    df %>%
      filter(date1 >= input$date_range[1] & date1 <= input$date_range[2]) %>%
      mutate(time = floor_date(date1, input$agg_level)) %>%
      group_by(time) %>%
      summarise(!!input$var_select := sum(!!sym(input$var_select)))
  })
  
  output$plot1 <- renderPlotly({
    req(input$plot)
    
    data <- get_filtered_data()
    
    plot <- ggplot(data, aes(x = time, y = !!sym(input$var_select), group = 1,
      text = paste("Date:", time, "<br>Value:", !!sym(input$var_select)))) +
      geom_line(color = input$line_color, linetype = input$line_type) +
      theme_minimal() +
      labs(x = "Time", y = input$var_select)
    
    ggplotly(plot, tooltip = "text")
  })
  
  # Original data download
  output$downloadOriginal <- downloadHandler(
    filename = function() {
      paste("original-data-", Sys.Date(), ".csv", sep="")
    },
    content = function(file) {
      write.csv(df, file, row.names = FALSE)
    }
  )
  
  # Filtered data download
  output$downloadFiltered <- downloadHandler(
    filename = function() {
      paste("filtered-data-", Sys.Date(), ".csv", sep="")
    },
    content = function(file) {
      write.csv(get_filtered_data(), file, row.names = FALSE)
    }
  )
  
}

shinyApp(ui = ui, server = server)