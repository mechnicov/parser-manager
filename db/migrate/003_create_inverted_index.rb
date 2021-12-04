class CreateInvertedIndex < ActiveRecord::Migration[6.1]
  def change
    create_table :inverted_index do |t|
      t.string :word, null: false
      t.integer :word_count, null: false
      t.belongs_to :page, null: false, foreign_key: true

      t.index %i[word page_id], unique: true

      t.timestamps
    end
  end
end
