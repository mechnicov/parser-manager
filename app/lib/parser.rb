require 'docx'
require 'msworddoc-extractor'

class Parser
  class << self
    def call(file:, content:, file_type:)
      case file_type
      when :pdf then new(file, content).from_pdf
      when :doc then new(file, content).from_doc
      when :docx then new(file, content).from_docx
      when :html then new(file, content).from_html
      end
    end
  end

  def initialize(file, content)
    @file = file
    @content = content
  end

  def from_pdf
    tmp_path = "#{file.path}.tmp"
    `pdftotext #{file.path} #{tmp_path} -layout`
    File.read(tmp_path).strip
  end

  def from_doc
    doc = MSWordDoc::Essence.new
    ole = Ole::Storage.open(file)
    doc.load_storage(ole)
    doc.whole_contents.strip
  end

  def from_docx
    Docx::Document.open(content).text
  rescue Errno::ENOENT
    raise ParseManager::UnsupportedFileTypeError
  end

  def from_html
    html = Nokogiri::HTML(content)
    html.css('script').remove
    html.css('footer').remove
    html.css('[class*="footer"]').remove
    html.css('body').text.strip
  end

  private

  attr_reader :file, :content
end
