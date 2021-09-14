require 'mimemagic'

class ParseManager
  class Error < StandardError; end

  class UnsupportedFileTypeError < Error
    def message
      'Unsupported file type'
    end
  end

  class << self
    def call(file:, url:)
      new(file, url).call
    end
  end

  PDF_MIMETYPE = 'application/pdf'.freeze
  DOC_MIMETYPE = 'application/msword'.freeze
  DOCX_MIMETYPE = %w[application/vnd.openxmlformats-officedocument.wordprocessingml.document application/zip].freeze
  HTML_MIMETYPE = 'text/html'.freeze

  def initialize(file, url)
    @file = file
    @url = url
  end

  def call
    identify_type
    persist(parsed_data: parsed_data, url: url)
  end

  private

  attr_reader :file, :content, :file_type, :url

  def identify_type
    @content = File.read(file)

    @file_type =
      case MimeMagic.by_magic(content).type
      when PDF_MIMETYPE then :pdf
      when DOC_MIMETYPE then :doc
      when *DOCX_MIMETYPE then :docx
      when HTML_MIMETYPE then :html
      else raise UnsupportedFileTypeError
      end
  end

  def parsed_data
    Parser.(file: file, content: content, file_type: file_type)
  end

  def persist(**args)
    Page.where(url: args[:url]).first_or_initialize.tap do |page|
      page.parsed_data = args[:parsed_data]
      page.file_type = file_type
      page.save
    end
  end
end
